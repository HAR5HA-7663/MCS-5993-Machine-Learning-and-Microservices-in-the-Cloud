# Job Portal API - RESTful Job Listing Platform

A complete RESTful API for a job listing and application platform similar to Indeed, built with FastAPI, Docker, and following REST best practices.

## 🎯 Features

### Core Functionality

- ✅ **Job Seekers Management** - Create profiles, upload resumes
- ✅ **Employers Management** - Company profiles and job posting
- ✅ **Job Postings** - Full CRUD with filtering (location, type, status)
- ✅ **Applications** - Submit applications with resume uploads
- ✅ **File Storage** - PDF resume storage and retrieval
- ✅ **HATEOAS** - Hypermedia links for resource navigation

### RESTful Design Principles

| Principle           | Implementation                                       |
| ------------------- | ---------------------------------------------------- |
| **Resource Naming** | Proper noun-based URLs (`/api/jobs`, `/api/seekers`) |
| **HTTP Methods**    | GET, POST, PUT, PATCH, DELETE correctly mapped       |
| **Statelessness**   | No server-side session storage                       |
| **HATEOAS**         | Related resource links in responses                  |
| **Status Codes**    | 200, 201, 204, 400, 404 appropriately used           |

## � Project Structure

```
job-portal-api/
├── app/                      # Application code
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models & schemas
│   ├── database.py          # Database connection & initialization
│   ├── requirements.txt     # Python dependencies
│   └── routes/              # API route handlers
│       ├── jobs.py         # Job posting endpoints
│       ├── employers.py    # Employer endpoints
│       ├── seekers.py      # Job seeker endpoints
│       └── applications.py # Application endpoints
├── scripts/                  # Utility scripts
│   ├── README.md            # Scripts documentation
│   ├── demo.sh             # Quick API demonstration
│   ├── test_api.sh         # Comprehensive test suite
│   └── inspect_db.sh       # Database inspection tool
├── docs/                     # Documentation
│   ├── README.md            # Documentation guide
│   ├── PROJECT_COMPLETE.md # Project completion summary
│   └── DATABASE_PERSISTENCE.md # Storage & persistence guide
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-container orchestration
└── README.md               # This file
```

## �🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Port 8000 available

### Run with Docker (Recommended)

```bash
# Navigate to project directory
cd job-portal-api

# Build and start the containers
docker compose up -d --build

# Wait for API to start
sleep 5

# Run demo to see it in action
./scripts/demo.sh

# Access the API
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Run Locally (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Run the application
cd app
uvicorn main:app --reload

# Access: http://localhost:8000/docs
```

## 📚 API Documentation

### Base URL

```
http://localhost:8000
```

### Main Endpoints

#### Job Seekers

```http
POST   /api/seekers              # Create job seeker profile
GET    /api/seekers              # List all seekers
GET    /api/seekers/{id}         # Get seeker details
PUT    /api/seekers/{id}         # Update seeker profile
DELETE /api/seekers/{id}         # Delete seeker
POST   /api/seekers/{id}/upload-resume  # Upload resume (PDF)
```

#### Employers

```http
POST   /api/employers            # Create employer profile
GET    /api/employers            # List all employers
GET    /api/employers/{id}       # Get employer details
PUT    /api/employers/{id}       # Update employer profile
DELETE /api/employers/{id}       # Delete employer
```

#### Job Postings

```http
POST   /api/jobs                 # Create job posting
GET    /api/jobs                 # List all jobs (with filters)
GET    /api/jobs/{id}            # Get job details
PUT    /api/jobs/{id}            # Update job posting
PATCH  /api/jobs/{id}/status     # Update job status
DELETE /api/jobs/{id}            # Delete job posting
GET    /api/jobs/{id}/applications  # Get job applications
```

**Query Parameters for GET /api/jobs:**

- `status` - Filter by status (open, closed, filled)
- `location` - Filter by location
- `job_type` - Filter by type (full-time, part-time, contract)
- `skip` - Pagination offset
- `limit` - Results per page

#### Applications

```http
POST   /api/applications         # Submit application
GET    /api/applications         # List applications (with filters)
GET    /api/applications/{id}    # Get application details
PATCH  /api/applications/{id}/status  # Update status (employer action)
DELETE /api/applications/{id}    # Withdraw application
POST   /api/applications/{id}/upload-resume  # Upload resume
```

**Query Parameters for GET /api/applications:**

- `seeker_id` - Filter by job seeker
- `job_id` - Filter by job posting
- `status` - Filter by status (pending, reviewed, accepted, rejected)

## 🧪 Testing the API

### Using Swagger UI

1. Open browser: http://localhost:8000/docs
2. Explore endpoints with interactive documentation
3. Click "Try it out" on any endpoint
4. Fill in parameters and execute requests

### Example Workflow

```bash
# 1. Create an employer
curl -X POST http://localhost:8000/api/employers \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Corp",
    "email": "hr@techcorp.com",
    "phone": "555-0100",
    "description": "Leading tech company",
    "website": "https://techcorp.com"
  }'

# 2. Create a job posting (use employer_id from response)
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "employer_id": 1,
    "title": "Senior Python Developer",
    "description": "Build scalable APIs",
    "requirements": ["Python", "FastAPI", "Docker"],
    "location": "Remote",
    "salary_range": "$100k-$150k",
    "job_type": "full-time",
    "experience_required": 5
  }'

# 3. Create a job seeker
curl -X POST http://localhost:8000/api/seekers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "skills": ["Python", "FastAPI", "React"],
    "experience_years": 6
  }'

# 4. Upload resume for seeker
curl -X POST http://localhost:8000/api/seekers/1/upload-resume \
  -F "file=@resume.pdf"

# 5. Apply for job
curl -X POST http://localhost:8000/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "seeker_id": 1,
    "cover_letter": "I am excited to apply..."
  }'
```

## 🏗️ Project Structure

```
job-portal-api/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models & schemas
│   ├── database.py          # Database setup & connection
│   ├── routes/
│   │   ├── jobs.py          # Job posting endpoints
│   │   ├── employers.py     # Employer endpoints
│   │   ├── seekers.py       # Job seeker endpoints
│   │   └── applications.py  # Application endpoints
│   ├── storage/             # File storage directory
│   │   ├── resumes/         # Job seeker resumes
│   │   └── application_resumes/  # Application resumes
│   └── requirements.txt
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Docker Compose setup
└── README.md
```

## 🗄️ Database Schema

### Tables

**job_seekers**

- id, name, email, phone, skills (JSON), experience_years, resume_url, created_at

**employers**

- id, company_name, email, phone, description, website, created_at

**job_postings**

- id, employer_id (FK), title, description, requirements (JSON), location, salary_range, job_type, experience_required, status, created_at, updated_at

**applications**

- id, job_id (FK), seeker_id (FK), cover_letter, resume_url, status, applied_at

## 📦 Docker Configuration

### Services

- **jobapi** - FastAPI application container
- **db** (optional) - PostgreSQL database (commented out by default)

### Volumes

- `./app` - Application code (for hot reload)
- `./app/storage` - Persistent file storage
- `./jobportal.db` - SQLite database file

### Environment Variables

- `PYTHONUNBUFFERED=1` - Real-time logging

## 🔧 Configuration

### Switch to PostgreSQL (Production)

1. Uncomment PostgreSQL service in `docker-compose.yml`
2. Install `psycopg2-binary` in `requirements.txt`
3. Update `database.py` to use PostgreSQL connection
4. Run migrations

```bash
docker-compose up --build
```

## 🎨 HATEOAS Implementation

Example response with hypermedia links:

```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "employer_id": 1,
  "status": "open",
  "links": {
    "self": "http://localhost:8000/api/jobs/1",
    "employer": "http://localhost:8000/api/employers/1",
    "applications": "http://localhost:8000/api/jobs/1/applications",
    "apply": "http://localhost:8000/api/applications"
  }
}
```

## 🛠️ Development Commands

```bash
# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild containers
docker-compose up --build

# Access container shell
docker exec -it job-portal-api bash

# Run database migrations (if using PostgreSQL)
docker-compose exec jobapi alembic upgrade head
```

## 📊 API Statistics

- **Total Endpoints**: 25+
- **Resource Types**: 4 (Seekers, Employers, Jobs, Applications)
- **HTTP Methods Used**: GET, POST, PUT, PATCH, DELETE
- **File Upload Support**: PDF resumes
- **Database**: SQLite (default) / PostgreSQL (optional)

## 🚦 Next Steps (Phase 6 - Kubernetes)

Ready to deploy to Kubernetes? Let me know when you want to proceed with:

- Kubernetes deployment configuration
- Service and Ingress setup
- Persistent volume claims
- Minikube local deployment

## 📝 Notes

- Default database: SQLite (`jobportal.db`)
- File storage: Local filesystem
- Authentication: Not implemented (add JWT for production)
- Rate limiting: Not implemented (add for production)

## 📚 Additional Documentation

For more detailed information, see:

- **[Scripts Documentation](scripts/README.md)** - How to use demo, test, and inspection scripts
- **[Project Completion Summary](docs/PROJECT_COMPLETE.md)** - Full project status and implementation details
- **[Database Persistence Guide](docs/DATABASE_PERSISTENCE.md)** - Storage, backup, and data management
- **[Resume Upload Guide](docs/RESUME_UPLOAD_GUIDE.md)** - How to upload resumes with applications
- **[Swagger File Upload Guide](docs/SWAGGER_FILE_UPLOAD.md)** - Step-by-step Swagger UI file upload
- **[Documentation Index](docs/README.md)** - Complete documentation navigation

### Quick Links
- 🔧 [Run Demo](scripts/demo.sh) - `./scripts/demo.sh`
- 🧪 [Run Tests](scripts/test_api.sh) - `./scripts/test_api.sh`
- 🔍 [Inspect Database](scripts/inspect_db.sh) - `./scripts/inspect_db.sh`
- 📖 [Swagger UI](http://localhost:8000/docs) - Interactive API docs
- 📘 [ReDoc](http://localhost:8000/redoc) - Clean API reference
- 📤 [Upload File in Swagger](docs/SWAGGER_FILE_UPLOAD.md) - File upload guide

## 🤝 Contributing

This is an assignment project demonstrating RESTful API design principles.

## 📄 License

MIT License - Educational purposes

---

**Last Updated**: October 4, 2025  
**Version**: 1.0.0  
**Status**: ✅ Phases 1-5 Complete | ⏸️ Phase 6 Pending
