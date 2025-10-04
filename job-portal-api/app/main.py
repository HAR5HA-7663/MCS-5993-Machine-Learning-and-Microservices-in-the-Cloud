from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from database import init_db
from routes import jobs, employers, seekers, applications

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Job Listing Platform API",
    description="""
    A RESTful API for a job listing and application platform similar to Indeed.
    
    ## Features
    
    * **Job Seekers** - Create profiles, upload resumes, apply for jobs
    * **Employers** - Create company profiles, post job listings
    * **Job Postings** - Full CRUD operations with filtering
    * **Applications** - Submit and track job applications
    * **File Storage** - Upload and store PDF resumes
    * **HATEOAS** - Hypermedia links for related resources
    
    ## RESTful Design Principles
    
    This API follows REST best practices:
    - **Resource-based URLs** - Clear noun-based endpoints
    - **HTTP Methods** - Proper use of GET, POST, PUT, PATCH, DELETE
    - **Stateless** - Each request contains all necessary information
    - **HATEOAS** - Links to related resources included in responses
    - **Status Codes** - Appropriate HTTP status codes for all responses
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(seekers.router)
app.include_router(employers.router)
app.include_router(jobs.router)
app.include_router(applications.router)

# Mount storage directories for static file access
STORAGE_DIR = "app/storage"
os.makedirs(f"{STORAGE_DIR}/resumes", exist_ok=True)
os.makedirs(f"{STORAGE_DIR}/application_resumes", exist_ok=True)

app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with HATEOAS links"""
    return {
        "message": "Welcome to Job Listing Platform API",
        "version": "1.0.0",
        "documentation": "http://localhost:8000/docs",
        "links": {
            "jobs": "/api/jobs",
            "seekers": "/api/seekers",
            "employers": "/api/employers",
            "applications": "/api/applications"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "job-portal-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
