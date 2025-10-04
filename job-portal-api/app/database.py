import sqlite3
from contextlib import contextmanager
import os

# Use environment variable or default path for persistence
DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/data/jobportal.db")

def init_db():
    """Initialize the database with required tables"""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Job Seekers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_seekers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            skills TEXT NOT NULL,
            experience_years INTEGER NOT NULL,
            resume_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Employers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            description TEXT NOT NULL,
            website TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Job Postings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employer_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            requirements TEXT NOT NULL,
            location TEXT NOT NULL,
            salary_range TEXT NOT NULL,
            job_type TEXT NOT NULL,
            experience_required INTEGER NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employer_id) REFERENCES employers(id)
        )
    """)
    
    # Applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            seeker_id INTEGER NOT NULL,
            cover_letter TEXT NOT NULL,
            resume_url TEXT,
            status TEXT DEFAULT 'pending',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES job_postings(id),
            FOREIGN KEY (seeker_id) REFERENCES job_seekers(id),
            UNIQUE(job_id, seeker_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized successfully at {DATABASE_PATH}!")

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_db():
    """Get database connection for dependency injection"""
    with get_db_connection() as conn:
        yield conn
