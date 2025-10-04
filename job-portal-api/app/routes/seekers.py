from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import json
from models import JobSeeker, JobSeekerCreate
from database import get_db_connection
import os
import shutil

router = APIRouter(prefix="/api/seekers", tags=["Job Seekers"])

UPLOAD_DIR = "/app/storage/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=JobSeeker, status_code=201)
async def create_job_seeker(seeker: JobSeekerCreate):
    """Create a new job seeker profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO job_seekers (name, email, phone, skills, experience_years)
                VALUES (?, ?, ?, ?, ?)
            """, (seeker.name, seeker.email, seeker.phone, 
                  json.dumps(seeker.skills), seeker.experience_years))
            
            seeker_id = cursor.lastrowid
            
            # Fetch the created seeker
            cursor.execute("SELECT * FROM job_seekers WHERE id = ?", (seeker_id,))
            row = cursor.fetchone()
            
            return {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "skills": json.loads(row["skills"]),
                "experience_years": row["experience_years"],
                "resume_url": row["resume_url"],
                "created_at": row["created_at"]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[JobSeeker])
async def get_all_seekers():
    """Get all job seekers"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_seekers ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "skills": json.loads(row["skills"]),
                "experience_years": row["experience_years"],
                "resume_url": row["resume_url"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

@router.get("/{seeker_id}", response_model=JobSeeker)
async def get_seeker(seeker_id: int):
    """Get a specific job seeker by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_seekers WHERE id = ?", (seeker_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Job seeker not found")
        
        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "skills": json.loads(row["skills"]),
            "experience_years": row["experience_years"],
            "resume_url": row["resume_url"],
            "created_at": row["created_at"]
        }

@router.put("/{seeker_id}", response_model=JobSeeker)
async def update_seeker(seeker_id: int, seeker: JobSeekerCreate):
    """Update a job seeker profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE job_seekers 
            SET name = ?, email = ?, phone = ?, skills = ?, experience_years = ?
            WHERE id = ?
        """, (seeker.name, seeker.email, seeker.phone, 
              json.dumps(seeker.skills), seeker.experience_years, seeker_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job seeker not found")
        
        cursor.execute("SELECT * FROM job_seekers WHERE id = ?", (seeker_id,))
        row = cursor.fetchone()
        
        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "skills": json.loads(row["skills"]),
            "experience_years": row["experience_years"],
            "resume_url": row["resume_url"],
            "created_at": row["created_at"]
        }

@router.delete("/{seeker_id}", status_code=204)
async def delete_seeker(seeker_id: int):
    """Delete a job seeker profile"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job_seekers WHERE id = ?", (seeker_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job seeker not found")

@router.post("/{seeker_id}/upload-resume")
async def upload_resume(seeker_id: int, file: UploadFile = File(...)):
    """Upload resume for a job seeker"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check if seeker exists
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM job_seekers WHERE id = ?", (seeker_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job seeker not found")
        
        # Save file
        filename = f"seeker_{seeker_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update database
        resume_url = f"/storage/resumes/{filename}"
        cursor.execute("UPDATE job_seekers SET resume_url = ? WHERE id = ?", 
                      (resume_url, seeker_id))
        
        return {
            "message": "Resume uploaded successfully",
            "resume_url": resume_url,
            "access_url": f"http://localhost:8000{resume_url}"
        }
