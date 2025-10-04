import psycopg2, os

DB_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")

def remove_all_data():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM cars;")
    conn.commit()
    cur.close()
    conn.close()
    print("All data removed from cars table.")

if __name__ == "__main__":
    remove_all_data()
