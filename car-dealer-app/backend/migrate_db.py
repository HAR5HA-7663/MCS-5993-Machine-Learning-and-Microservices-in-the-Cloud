import psycopg2
import os

DB_URL = os.getenv("DATABASE_URL", "dbname=cardb user=caruser password=carpass host=db")

def migrate():
    print("Starting database migration...")
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        # Check if added_at column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='cars' AND column_name='added_at';
        """)
        
        if cur.fetchone() is None:
            print("Adding 'added_at' column to cars table...")
            cur.execute("""
                ALTER TABLE cars 
                ADD COLUMN added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)
            
            # Update existing rows with current timestamp
            cur.execute("""
                UPDATE cars 
                SET added_at = CURRENT_TIMESTAMP 
                WHERE added_at IS NULL;
            """)
            
            conn.commit()
            print("✅ Migration completed successfully!")
        else:
            print("✅ Column 'added_at' already exists. No migration needed.")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    migrate()
