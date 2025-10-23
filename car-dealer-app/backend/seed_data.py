import psycopg2, random, string, os

DB_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")

brand_models = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Prius", "Tacoma", "Sienna"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit", "Ridgeline", "Odyssey"],
    "Ford": ["F-150", "Mustang", "Explorer", "Focus", "Edge", "Escape", "Bronco"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "X1", "7 Series", "i4"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Accent", "Venue"],
    "Kia": ["Sorento", "Sportage", "Optima", "Soul", "Forte", "Stinger"],
    "Chevrolet": ["Malibu", "Impala", "Equinox", "Tahoe", "Silverado", "Camaro"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Maxima", "Frontier"],
    "Mercedes": ["C-Class", "E-Class", "GLC", "GLE", "A-Class", "S-Class"],
    "Audi": ["A4", "Q5", "A6", "Q7", "A3", "e-tron"],
    "Lexus": ["ES", "RX", "NX", "GX", "LS", "LC"],
    "Mazda": ["CX-5", "Mazda3", "CX-9", "MX-5 Miata", "CX-30"],
    "Subaru": ["Outback", "Forester", "Impreza", "Crosstrek", "Legacy"],
    "Volkswagen": ["Jetta", "Passat", "Tiguan", "Golf", "Atlas"]
}

brands = list(brand_models.keys())

def random_vin():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))

def seed_data():
    print("Starting seed_data")
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            vin VARCHAR(20) PRIMARY KEY,
            year INT,
            brand TEXT,
            model TEXT,
            mileage INT,
            price INT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM cars;")
    count_before = cur.fetchone()[0]
    print(f"Existing cars in database: {count_before}")
    import sys
    sys.stdout.flush()

    print("Adding new cars without clearing existing data...")

    for _ in range(50):
        vin = random_vin()
        year = random.randint(2005, 2024)
        brand = random.choice(brands)
        model = random.choice(brand_models[brand])
        mileage = random.randint(10000, 150000)
        price = random.randint(5000, 80000)

        cur.execute(
            "INSERT INTO cars (vin, year, brand, model, mileage, price) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (vin, year, brand, model, mileage, price)
        )

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM cars;")
    count_after = cur.fetchone()[0]
    added_count = count_after - count_before
    print(f"Total cars after seeding: {count_after}")
    print(f"Successfully added {added_count} new cars!")
    conn.close()

if __name__ == "__main__":
    seed_data()
