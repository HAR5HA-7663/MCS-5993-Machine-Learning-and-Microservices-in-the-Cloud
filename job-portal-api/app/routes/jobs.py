from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import json
from models import JobPosting, JobPostingCreate, JobPostingWithLinks, JobStatus
from database import get_db_connection

router = APIRouter(prefix="/api/jobs", tags=["Job Postings"])

def add_hateoas_links(job: dict, base_url: str = "http://localhost:8000") -> dict:
    """Add HATEOAS links to job posting"""
    job["links"] = {
        "self": f"{base_url}/api/jobs/{job['id']}",
        "employer": f"{base_url}/api/employers/{job['employer_id']}",
        "applications": f"{base_url}/api/jobs/{job['id']}/applications",
        "apply": f"{base_url}/api/applications"
    }
    return job

@router.post("/", response_model=JobPostingWithLinks, status_code=201)
async def create_job_posting(job: JobPostingCreate):
    """Create a new job posting"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Verify employer exists
        cursor.execute("SELECT id FROM employers WHERE id = ?", (job.employer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employer not found")
        
        try:
            cursor.execute("""
                INSERT INTO job_postings 
                (employer_id, title, description, requirements, location, 
                 salary_range, job_type, experience_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (job.employer_id, job.title, job.description, 
                  json.dumps(job.requirements), job.location, 
                  job.salary_range, job.job_type, job.experience_required))
            
            job_id = cursor.lastrowid
            
            # Fetch the created job
            cursor.execute("SELECT * FROM job_postings WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            
            result = {
                "id": row["id"],
                "employer_id": row["employer_id"],
                "title": row["title"],
                "description": row["description"],
                "requirements": json.loads(row["requirements"]),
                "location": row["location"],
                "salary_range": row["salary_range"],
                "job_type": row["job_type"],
                "experience_required": row["experience_required"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
            return add_hateoas_links(result)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[JobPostingWithLinks])
async def get_all_jobs(
    status: Optional[JobStatus] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get all job postings with optional filters"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM job_postings WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status.value)
        
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        
        if job_type:
            query += " AND job_type = ?"
            params.append(job_type)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        jobs = [
            {
                "id": row["id"],
                "employer_id": row["employer_id"],
                "title": row["title"],
                "description": row["description"],
                "requirements": json.loads(row["requirements"]),
                "location": row["location"],
                "salary_range": row["salary_range"],
                "job_type": row["job_type"],
                "experience_required": row["experience_required"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            for row in rows
        ]
        
        return [add_hateoas_links(job) for job in jobs]

@router.get("/{job_id}", response_model=JobPostingWithLinks)
async def get_job(job_id: int):
    """Get a specific job posting by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        result = {
            "id": row["id"],
            "employer_id": row["employer_id"],
            "title": row["title"],
            "description": row["description"],
            "requirements": json.loads(row["requirements"]),
            "location": row["location"],
            "salary_range": row["salary_range"],
            "job_type": row["job_type"],
            "experience_required": row["experience_required"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        
        return add_hateoas_links(result)

@router.put("/{job_id}", response_model=JobPostingWithLinks)
async def update_job(job_id: int, job: JobPostingCreate):
    """Update a job posting"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE job_postings 
            SET title = ?, description = ?, requirements = ?, location = ?, 
                salary_range = ?, job_type = ?, experience_required = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (job.title, job.description, json.dumps(job.requirements), 
              job.location, job.salary_range, job.job_type, 
              job.experience_required, job_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        cursor.execute("SELECT * FROM job_postings WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        
        result = {
            "id": row["id"],
            "employer_id": row["employer_id"],
            "title": row["title"],
            "description": row["description"],
            "requirements": json.loads(row["requirements"]),
            "location": row["location"],
            "salary_range": row["salary_range"],
            "job_type": row["job_type"],
            "experience_required": row["experience_required"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        
        return add_hateoas_links(result)

@router.patch("/{job_id}/status")
async def update_job_status(job_id: int, status: JobStatus):
    """Update job posting status (open/closed/filled)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE job_postings 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status.value, job_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        return {"message": f"Job status updated to {status.value}"}

@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: int):
    """Delete a job posting"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job_postings WHERE id = ?", (job_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job posting not found")

@router.get("/{job_id}/applications")
async def get_job_applications(job_id: int):
    """Get all applications for a specific job"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Verify job exists
        cursor.execute("SELECT id FROM job_postings WHERE id = ?", (job_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        cursor.execute("""
            SELECT a.*, js.name as seeker_name, js.email as seeker_email
            FROM applications a
            JOIN job_seekers js ON a.seeker_id = js.id
            WHERE a.job_id = ?
            ORDER BY a.applied_at DESC
        """, (job_id,))
        
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "job_id": row["job_id"],
                "seeker_id": row["seeker_id"],
                "seeker_name": row["seeker_name"],
                "seeker_email": row["seeker_email"],
                "cover_letter": row["cover_letter"],
                "resume_url": row["resume_url"],
                "status": row["status"],
                "applied_at": row["applied_at"]
            }
            for row in rows
        ]
