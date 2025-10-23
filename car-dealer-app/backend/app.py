from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Handle both old and new DATABASE_URL formats
DATABASE_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")
if DATABASE_URL.startswith("postgresql://"):
    # Convert PostgreSQL URL to psycopg2 format
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    DB_URL = f"dbname={url.path[1:]} user={url.username} password={url.password} host={url.hostname} port={url.port or 5432}"
else:
    DB_URL = DATABASE_URL

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/cars", methods=["GET"])
def get_cars():
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    # Get sorting parameters
    sort_by = request.args.get("sort_by", "year")  # Default sort by year
    sort_order = request.args.get("sort_order", "DESC")  # Default descending
    
    # Validate sort parameters
    allowed_columns = ["year", "brand", "model", "price", "mileage", "added_at"]
    if sort_by not in allowed_columns:
        sort_by = "year"
    
    if sort_order.upper() not in ["ASC", "DESC"]:
        sort_order = "DESC"

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM cars")
    total = cur.fetchone()[0]

    # Build dynamic query with sorting
    query = f"""
        SELECT vin, year, brand, model, mileage, price, added_at 
        FROM cars 
        ORDER BY {sort_by} {sort_order} 
        LIMIT %s OFFSET %s
    """
    cur.execute(query, (per_page, offset))
    rows = cur.fetchall()
    conn.close()

    cars = [
        {
            "vin": r[0], 
            "year": r[1], 
            "brand": r[2], 
            "model": r[3], 
            "mileage": r[4], 
            "price": r[5],
            "added_at": r[6].isoformat() if r[6] else None
        }
        for r in rows
    ]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "cars": cars,
        "sort_by": sort_by,
        "sort_order": sort_order
    })

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["vin", "year", "brand", "model", "mileage", "price"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO cars (vin, year, brand, model, mileage, price) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["vin"], data["year"], data["brand"], data["model"], data["mileage"], data["price"])
        )
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Car added successfully", "vin": data["vin"]}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Car with this VIN already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cars", methods=["DELETE"])
def delete_cars():
    data = request.get_json()
    vins = data.get("vins", [])
    
    if not vins:
        return jsonify({"error": "No VINs provided"}), 400
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Delete cars with the provided VINs
        cur.execute("DELETE FROM cars WHERE vin = ANY(%s)", (vins,))
        deleted_count = cur.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({"message": f"Successfully deleted {deleted_count} car(s)", "count": deleted_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cars/<string:vin>", methods=["GET"])
def get_car_by_vin(vin):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("SELECT vin, year, brand, model, mileage, price, added_at FROM cars WHERE vin = %s", (vin,))
        row = cur.fetchone()
        conn.close()
        
        if row:
            car = {
                "vin": row[0], 
                "year": row[1], 
                "brand": row[2], 
                "model": row[3], 
                "mileage": row[4], 
                "price": row[5],
                "added_at": row[6].isoformat() if row[6] else None
            }
            return jsonify(car)
        else:
            return jsonify({"error": "Car not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching car {vin}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/cars/<string:vin>", methods=["PUT"])
def update_car(vin):
    data = request.get_json()
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Check if car exists
        cur.execute("SELECT vin FROM cars WHERE vin = %s", (vin,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"error": "Car not found"}), 404
        
        # Update car
        cur.execute(
            """UPDATE cars SET year = %s, brand = %s, model = %s, mileage = %s, price = %s 
               WHERE vin = %s""",
            (data.get("year"), data.get("brand"), data.get("model"), 
             data.get("mileage"), data.get("price"), vin)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Car updated successfully", "vin": vin})
    except Exception as e:
        logger.error(f"Error updating car {vin}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Total cars
        cur.execute("SELECT COUNT(*) FROM cars")
        total_cars = cur.fetchone()[0]
        
        # Average price
        cur.execute("SELECT AVG(price) FROM cars")
        avg_price = cur.fetchone()[0] or 0
        
        # Average mileage
        cur.execute("SELECT AVG(mileage) FROM cars")
        avg_mileage = cur.fetchone()[0] or 0
        
        # Most expensive car
        cur.execute("SELECT brand, model, price FROM cars ORDER BY price DESC LIMIT 1")
        most_expensive = cur.fetchone()
        
        # Car count by brand
        cur.execute("SELECT brand, COUNT(*) FROM cars GROUP BY brand ORDER BY COUNT(*) DESC")
        brand_counts = cur.fetchall()
        
        # Cars by year range
        cur.execute("""
            SELECT 
                CASE 
                    WHEN year >= 2020 THEN 'New (2020+)'
                    WHEN year >= 2015 THEN 'Recent (2015-2019)'
                    WHEN year >= 2010 THEN 'Older (2010-2014)'
                    ELSE 'Classic (Pre-2010)'
                END as age_group,
                COUNT(*) 
            FROM cars 
            GROUP BY age_group 
            ORDER BY MIN(year) DESC
        """)
        age_groups = cur.fetchall()
        
        conn.close()
        
        return jsonify({
            "total_cars": total_cars,
            "average_price": round(avg_price, 2),
            "average_mileage": round(avg_mileage, 0),
            "most_expensive": {
                "brand": most_expensive[0] if most_expensive else None,
                "model": most_expensive[1] if most_expensive else None,
                "price": most_expensive[2] if most_expensive else None
            },
            "brands": [{"brand": b[0], "count": b[1]} for b in brand_counts],
            "age_groups": [{"group": a[0], "count": a[1]} for a in age_groups]
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["GET"])
def search_cars():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        search_pattern = f"%{query}%"
        
        # Count total results
        cur.execute("""
            SELECT COUNT(*) FROM cars 
            WHERE LOWER(brand) LIKE LOWER(%s) 
               OR LOWER(model) LIKE LOWER(%s) 
               OR LOWER(vin) LIKE LOWER(%s)
               OR CAST(year as TEXT) LIKE %s
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        total = cur.fetchone()[0]
        
        # Get paginated results
        cur.execute("""
            SELECT vin, year, brand, model, mileage, price, added_at 
            FROM cars 
            WHERE LOWER(brand) LIKE LOWER(%s) 
               OR LOWER(model) LIKE LOWER(%s) 
               OR LOWER(vin) LIKE LOWER(%s)
               OR CAST(year as TEXT) LIKE %s
            ORDER BY year DESC 
            LIMIT %s OFFSET %s
        """, (search_pattern, search_pattern, search_pattern, search_pattern, per_page, offset))
        
        rows = cur.fetchall()
        conn.close()
        
        cars = [
            {
                "vin": r[0], 
                "year": r[1], 
                "brand": r[2], 
                "model": r[3], 
                "mileage": r[4], 
                "price": r[5],
                "added_at": r[6].isoformat() if r[6] else None
            }
            for r in rows
        ]
        
        return jsonify({
            "query": query,
            "page": page,
            "per_page": per_page,
            "total": total,
            "cars": cars
        })
    except Exception as e:
        logger.error(f"Error searching cars: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/seed", methods=["POST"])
def seed_database():
    """Endpoint to seed the database with sample cars"""
    try:
        # Import and run the existing seed_data function
        import subprocess
        import sys
        
        logger.info("Starting database seeding...")
        
        # Run the seed_data.py script
        result = subprocess.run([sys.executable, "seed_data.py"], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            logger.info("Seeding completed successfully")
            return jsonify({
                "message": "Database seeded successfully", 
                "output": result.stdout,
                "status": "success"
            }), 200
        else:
            logger.error(f"Seeding failed: {result.stderr}")
            return jsonify({
                "error": "Seeding failed", 
                "details": result.stderr,
                "status": "error"
            }), 500
            
    except Exception as e:
        logger.error(f"Error during seeding: {str(e)}")
        return jsonify({"error": f"Seeding error: {str(e)}", "status": "error"}), 500

@app.route("/erase", methods=["DELETE"])
def erase_database():
    """Endpoint to erase all cars from the database"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Count existing cars
        cur.execute("SELECT COUNT(*) FROM cars")
        count_before = cur.fetchone()[0]
        
        # Delete all cars
        cur.execute("DELETE FROM cars")
        conn.commit()
        
        # Verify deletion
        cur.execute("SELECT COUNT(*) FROM cars")
        count_after = cur.fetchone()[0]
        
        conn.close()
        
        logger.info(f"Database erased: {count_before} cars removed")
        
        return jsonify({
            "message": f"Successfully erased {count_before} cars from database",
            "cars_removed": count_before,
            "remaining_cars": count_after,
            "status": "success"
        }), 200
        
    except Exception as e:
        logger.error(f"Error during database erase: {str(e)}")
        return jsonify({"error": f"Erase error: {str(e)}", "status": "error"}), 500

@app.route("/health")
def health():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        conn.close()
        return {"status": "ok", "database": "connected", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
