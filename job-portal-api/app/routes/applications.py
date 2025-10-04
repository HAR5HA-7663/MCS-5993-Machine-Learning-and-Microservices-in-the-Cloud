from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from models import Application, ApplicationCreate, ApplicationStatus, ApplicationWithLinks
from database import get_db_connection
import os
import shutil

router = APIRouter(prefix="/api/applications", tags=["Applications"])

UPLOAD_DIR = "/app/storage/application_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def add_hateoas_links(app: dict, base_url: str = "http://localhost:8000") -> dict:
    """Add HATEOAS links to application"""
    app["links"] = {
        "self": f"{base_url}/api/applications/{app['id']}",
        "job": f"{base_url}/api/jobs/{app['job_id']}",
        "seeker": f"{base_url}/api/seekers/{app['seeker_id']}",
        "update_status": f"{base_url}/api/applications/{app['id']}/status"
    }
    return app

@router.post("/", response_model=ApplicationWithLinks, status_code=201)
async def create_application(application: ApplicationCreate):
    """Submit a job application"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Verify job exists and is open
        cursor.execute("SELECT status FROM job_postings WHERE id = ?", (application.job_id,))
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Job posting not found")
        if job["status"] != "open":
            raise HTTPException(status_code=400, detail="Job posting is not open for applications")
        
        # Verify seeker exists
        cursor.execute("SELECT id FROM job_seekers WHERE id = ?", (application.seeker_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job seeker not found")
        
        # Check for duplicate application
        cursor.execute("""
            SELECT id FROM applications 
            WHERE job_id = ? AND seeker_id = ?
        """, (application.job_id, application.seeker_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="You have already applied to this job")
        
        try:
            cursor.execute("""
                INSERT INTO applications (job_id, seeker_id, cover_letter)
                VALUES (?, ?, ?)
            """, (application.job_id, application.seeker_id, application.cover_letter))
            
            app_id = cursor.lastrowid
            
            # Fetch the created application
            cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
            row = cursor.fetchone()
            
            result = {
                "id": row["id"],
                "job_id": row["job_id"],
                "seeker_id": row["seeker_id"],
                "cover_letter": row["cover_letter"],
                "resume_url": row["resume_url"],
                "status": row["status"],
                "applied_at": row["applied_at"]
            }
            
            return add_hateoas_links(result)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ApplicationWithLinks])
async def get_all_applications(
    seeker_id: Optional[int] = None,
    job_id: Optional[int] = None,
    status: Optional[ApplicationStatus] = None
):
    """Get all applications with optional filters"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM applications WHERE 1=1"
        params = []
        
        if seeker_id:
            query += " AND seeker_id = ?"
            params.append(seeker_id)
        
        if job_id:
            query += " AND job_id = ?"
            params.append(job_id)
        
        if status:
            query += " AND status = ?"
            params.append(status.value)
        
        query += " ORDER BY applied_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        applications = [
            {
                "id": row["id"],
                "job_id": row["job_id"],
                "seeker_id": row["seeker_id"],
                "cover_letter": row["cover_letter"],
                "resume_url": row["resume_url"],
                "status": row["status"],
                "applied_at": row["applied_at"]
            }
            for row in rows
        ]
        
        return [add_hateoas_links(app) for app in applications]

@router.get("/{application_id}", response_model=ApplicationWithLinks)
async def get_application(application_id: int):
    """Get a specific application by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE id = ?", (application_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Application not found")
        
        result = {
            "id": row["id"],
            "job_id": row["job_id"],
            "seeker_id": row["seeker_id"],
            "cover_letter": row["cover_letter"],
            "resume_url": row["resume_url"],
            "status": row["status"],
            "applied_at": row["applied_at"]
        }
        
        return add_hateoas_links(result)

@router.patch("/{application_id}/status")
async def update_application_status(application_id: int, status: ApplicationStatus):
    """Update application status (for employers to review applications)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE applications 
            SET status = ?
            WHERE id = ?
        """, (status.value, application_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"message": f"Application status updated to {status.value}"}

@router.delete("/{application_id}", status_code=204)
async def delete_application(application_id: int):
    """Withdraw an application"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Application not found")

@router.post("/{application_id}/upload-resume")
async def upload_application_resume(application_id: int, file: UploadFile = File(...)):
    """Upload resume for a specific application"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM applications WHERE id = ?", (application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Save file
        filename = f"application_{application_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update database
        resume_url = f"/storage/application_resumes/{filename}"
        cursor.execute("UPDATE applications SET resume_url = ? WHERE id = ?", 
                      (resume_url, application_id))
        
        return {
            "message": "Resume uploaded successfully",
            "resume_url": resume_url,
            "access_url": f"http://localhost:8000{resume_url}"
        }
