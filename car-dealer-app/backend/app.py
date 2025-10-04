from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
DB_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")

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

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
