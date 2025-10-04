# 📄 Resume Upload Guide

Complete guide for uploading resumes with job applications in the Job Portal API.

---

## 🎯 Overview

There are **two ways** to upload resumes:

1. **Job Seeker Profile Resume** - Upload directly to seeker profile
2. **Application Resume** - Upload when applying for a specific job

---

## 📝 Method 1: Upload to Job Seeker Profile

### Endpoint

```
POST /api/seekers/{seeker_id}/upload-resume
```

### When to Use

- Job seeker wants to add a general resume to their profile
- Resume can be used for multiple applications

### Example

```bash
# Create a job seeker first
SEEKER_ID=1

# Upload resume to their profile
curl -X POST "http://localhost:8000/api/seekers/$SEEKER_ID/upload-resume" \
  -F "file=@/path/to/your/resume.pdf"
```

### Response

```json
{
  "message": "Resume uploaded successfully",
  "resume_url": "/storage/resumes/seeker_1_resume.pdf",
  "access_url": "http://localhost:8000/storage/resumes/seeker_1_resume.pdf"
}
```

---

## 📋 Method 2: Upload with Application

### Two-Step Process

#### Step 1: Create Application

```bash
# Submit application without resume first
curl -X POST "http://localhost:8000/api/applications/" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "seeker_id": 1,
    "cover_letter": "I am very interested in this position..."
  }'
```

**Response:**

```json
{
  "id": 1,
  "job_id": 1,
  "seeker_id": 1,
  "cover_letter": "I am very interested in this position...",
  "resume_url": null,
  "status": "pending",
  "applied_at": "2025-10-04T16:00:00"
}
```

#### Step 2: Upload Resume to Application

```bash
# Upload resume to the application
APPLICATION_ID=1

curl -X POST "http://localhost:8000/api/applications/$APPLICATION_ID/upload-resume" \
  -F "file=@/path/to/your/resume.pdf"
```

**Response:**

```json
{
  "message": "Resume uploaded successfully",
  "resume_url": "/storage/application_resumes/application_1_resume.pdf",
  "access_url": "http://localhost:8000/storage/application_resumes/application_1_resume.pdf"
}
```

---

## 🧪 Testing with Scripts

### Using demo.sh (Now includes resume upload!)

```bash
./scripts/demo.sh
```

This will:

1. ✅ Create employer, seeker, and job
2. ✅ Submit application
3. ✅ **Upload PDF resume automatically** (NEW!)
4. ✅ Verify the resume is attached

### Using test_api.sh (Comprehensive testing)

```bash
./scripts/test_api.sh
```

This will:

1. ✅ Create test data
2. ✅ Create a PDF resume file
3. ✅ Submit application
4. ✅ Upload resume to application
5. ✅ Verify application has resume URL

---

## 📂 File Requirements

### Accepted Format

- **Only PDF files** are allowed (`.pdf` extension)
- Other formats will be rejected with 400 error

### File Naming

- **Profile Resume**: `seeker_{id}_{filename}`
- **Application Resume**: `application_{id}_{filename}`

### Storage Locations

- **Profile Resumes**: `/app/storage/resumes/`
- **Application Resumes**: `/app/storage/application_resumes/`

Both are persisted in Docker volumes!

---

## 🔍 Verification

### Check if Resume is Attached

```bash
# Get application details
curl http://localhost:8000/api/applications/1 | jq
```

**Look for `resume_url` field:**

```json
{
  "id": 1,
  "job_id": 1,
  "seeker_id": 1,
  "cover_letter": "...",
  "resume_url": "/storage/application_resumes/application_1_resume.pdf",  ← Should not be null
  "status": "pending"
}
```

### Access the Resume File

```bash
# Download/view the resume
curl http://localhost:8000/storage/application_resumes/application_1_resume.pdf -o downloaded_resume.pdf

# Or open in browser:
# http://localhost:8000/storage/application_resumes/application_1_resume.pdf
```

---

## 💡 Complete Example Workflow

### Full Application with Resume

```bash
#!/bin/bash

API_BASE="http://localhost:8000"

# 1. Create Job Seeker
SEEKER=$(curl -s -X POST "$API_BASE/api/seekers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "skills": ["Python", "FastAPI"],
    "experience_years": 3
  }')
SEEKER_ID=$(echo $SEEKER | jq -r '.id')
echo "✓ Created Seeker (ID: $SEEKER_ID)"

# 2. Submit Application
APP=$(curl -s -X POST "$API_BASE/api/applications/" \
  -H "Content-Type: application/json" \
  -d "{
    \"job_id\": 1,
    \"seeker_id\": $SEEKER_ID,
    \"cover_letter\": \"I am very excited about this opportunity!\"
  }")
APP_ID=$(echo $APP | jq -r '.id')
echo "✓ Created Application (ID: $APP_ID)"

# 3. Upload Resume (Assuming you have resume.pdf)
UPLOAD=$(curl -s -X POST "$API_BASE/api/applications/$APP_ID/upload-resume" \
  -F "file=@resume.pdf")
echo "✓ Resume uploaded!"
echo $UPLOAD | jq

# 4. Verify
curl -s "$API_BASE/api/applications/$APP_ID" | jq '.resume_url'
```

---

## 🎨 Creating Test PDF Resumes

### Method 1: Simple Text to PDF (For Testing)

The demo script creates a minimal valid PDF:

```bash
cat > test_resume.pdf << 'EOF'
%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>>>endobj
4 0 obj<</Length 150>>stream
BT
/F1 14 Tf
50 700 Td
(YOUR NAME - RESUME) Tj
0 -30 Td
(Your details here) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer<</Size 5/Root 1 0 R>>
startxref
467
%%EOF
EOF
```

### Method 2: Use Real Resume

```bash
# Just upload your actual resume.pdf
curl -X POST "http://localhost:8000/api/applications/1/upload-resume" \
  -F "file=@/path/to/your/real_resume.pdf"
```

---

## 🔧 Using with Swagger UI

### Interactive Upload

1. Go to http://localhost:8000/docs
2. Find `POST /api/applications/{application_id}/upload-resume`
3. Click "Try it out"
4. Enter application ID
5. Click "Choose File" and select your PDF
6. Click "Execute"

---

## ❌ Common Errors

### Error: "Only PDF files are allowed"

**Cause**: File doesn't have `.pdf` extension  
**Solution**: Ensure file ends with `.pdf`

### Error: "Application not found"

**Cause**: Invalid application ID  
**Solution**: Create application first, use correct ID

### Error: "File too large"

**Cause**: Resume file is too big (if limits set)  
**Solution**: Compress PDF or use smaller file

---

## 🗂️ Resume Storage

### Persistence

Both resume storage locations are persisted in Docker volumes:

```yaml
volumes:
  - storage_data:/app/storage
```

### Check Stored Resumes

```bash
# List application resumes
docker exec job-portal-api ls -lh /app/storage/application_resumes/

# List profile resumes
docker exec job-portal-api ls -lh /app/storage/resumes/
```

### Backup Resumes

```bash
# Copy resumes from container to host
docker cp job-portal-api:/app/storage/application_resumes ./backup_resumes/
```

---

## 📊 API Endpoints Summary

| Endpoint                                  | Method | Purpose                   |
| ----------------------------------------- | ------ | ------------------------- |
| `/api/seekers/{id}/upload-resume`         | POST   | Upload to seeker profile  |
| `/api/applications/{id}/upload-resume`    | POST   | Upload to application     |
| `/storage/resumes/{filename}`             | GET    | Access profile resume     |
| `/storage/application_resumes/{filename}` | GET    | Access application resume |

---

## ✅ Verification Checklist

- [ ] Create application successfully
- [ ] Upload resume PDF
- [ ] Check `resume_url` is not null
- [ ] Access resume via URL
- [ ] Resume persists after container restart
- [ ] Run `./scripts/demo.sh` to see full flow
- [ ] Use Swagger UI to test upload

---

## 🎯 Quick Commands

```bash
# Run demo with resume upload
./scripts/demo.sh

# Run tests with resume upload
./scripts/test_api.sh

# Check application has resume
curl http://localhost:8000/api/applications/1 | jq '.resume_url'

# Download resume
curl http://localhost:8000/storage/application_resumes/application_1_resume.pdf -o resume.pdf

# List all resumes in container
docker exec job-portal-api ls -lh /app/storage/application_resumes/
```

---

## 📖 Additional Resources

- **Swagger UI**: http://localhost:8000/docs
- **Main README**: `../README.md`
- **Scripts Guide**: `scripts/README.md`
- **API Documentation**: `docs/PROJECT_COMPLETE.md`

---

**Last Updated**: October 4, 2025  
**Status**: ✅ Resume Upload Fully Functional
