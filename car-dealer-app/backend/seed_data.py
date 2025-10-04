import psycopg2, random, string, os

DB_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")

brand_models = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
    "Ford": ["F-150", "Mustang", "Explorer", "Focus"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
    "Kia": ["Sorento", "Sportage", "Optima", "Soul"],
    "Chevrolet": ["Malibu", "Impala", "Equinox", "Tahoe"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder"],
    "Mercedes": ["C-Class", "E-Class", "GLC", "GLE"]
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
    print(f"Entries before clearing: {count_before}")
    import sys
    sys.stdout.flush()

    cur.execute("DELETE FROM cars;")
    conn.commit()
    print("Cleared existing data.")

    cur.execute("SELECT COUNT(*) FROM cars;")
    count_after_clear = cur.fetchone()[0]
    print(f"Entries after clearing: {count_after_clear}")

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
    print(f"Entries after seeding: {count_after}")
    conn.close()
    print("Seeded 50 cars into database.")

if __name__ == "__main__":
    seed_data()
