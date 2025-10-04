from fastapi import APIRouter, HTTPException
from typing import List
from models import Employer, EmployerCreate
from database import get_db_connection

router = APIRouter(prefix="/api/employers", tags=["Employers"])

@router.post("/", response_model=Employer, status_code=201)
async def create_employer(employer: EmployerCreate):
    """Create a new employer profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO employers (company_name, email, phone, description, website)
                VALUES (?, ?, ?, ?, ?)
            """, (employer.company_name, employer.email, employer.phone, 
                  employer.description, employer.website))
            
            employer_id = cursor.lastrowid
            
            # Fetch the created employer
            cursor.execute("SELECT * FROM employers WHERE id = ?", (employer_id,))
            row = cursor.fetchone()
            
            return {
                "id": row["id"],
                "company_name": row["company_name"],
                "email": row["email"],
                "phone": row["phone"],
                "description": row["description"],
                "website": row["website"],
                "created_at": row["created_at"]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Employer])
async def get_all_employers():
    """Get all employers"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employers ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "company_name": row["company_name"],
                "email": row["email"],
                "phone": row["phone"],
                "description": row["description"],
                "website": row["website"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

@router.get("/{employer_id}", response_model=Employer)
async def get_employer(employer_id: int):
    """Get a specific employer by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employers WHERE id = ?", (employer_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Employer not found")
        
        return {
            "id": row["id"],
            "company_name": row["company_name"],
            "email": row["email"],
            "phone": row["phone"],
            "description": row["description"],
            "website": row["website"],
            "created_at": row["created_at"]
        }

@router.put("/{employer_id}", response_model=Employer)
async def update_employer(employer_id: int, employer: EmployerCreate):
    """Update an employer profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE employers 
            SET company_name = ?, email = ?, phone = ?, description = ?, website = ?
            WHERE id = ?
        """, (employer.company_name, employer.email, employer.phone, 
              employer.description, employer.website, employer_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employer not found")
        
        cursor.execute("SELECT * FROM employers WHERE id = ?", (employer_id,))
        row = cursor.fetchone()
        
        return {
            "id": row["id"],
            "company_name": row["company_name"],
            "email": row["email"],
            "phone": row["phone"],
            "description": row["description"],
            "website": row["website"],
            "created_at": row["created_at"]
        }

@router.delete("/{employer_id}", status_code=204)
async def delete_employer(employer_id: int):
    """Delete an employer profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employers WHERE id = ?", (employer_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employer not found")
