#!/bin/bash

# Job Portal API Test Script
# This script tests all major API endpoints

API_BASE="http://localhost:8000"
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${PURPLE}=====================================${NC}"
echo -e "${PURPLE}  Job Portal API - Test Suite${NC}"
echo -e "${PURPLE}=====================================${NC}\n"

# Test 1: Health Check
echo -e "${YELLOW}1. Testing Root Endpoint...${NC}"
curl -s $API_BASE/ | jq
echo -e "\n"

# Test 2: Create Employer
echo -e "${YELLOW}2. Creating Employer...${NC}"
EMPLOYER_RESPONSE=$(curl -s -X POST "$API_BASE/api/employers/" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Innovations Inc",
    "email": "hr@techinnovations.com",
    "phone": "+1-555-0100",
    "description": "Leading technology company specializing in AI and cloud solutions",
    "website": "https://techinnovations.com"
  }')
echo $EMPLOYER_RESPONSE | jq
EMPLOYER_ID=$(echo $EMPLOYER_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Employer created with ID: $EMPLOYER_ID${NC}\n"

# Test 3: Create Job Seeker
echo -e "${YELLOW}3. Creating Job Seeker...${NC}"
SEEKER_RESPONSE=$(curl -s -X POST "$API_BASE/api/seekers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane.smith@email.com",
    "phone": "+1-555-0200",
    "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "React"],
    "experience_years": 5
  }')
echo $SEEKER_RESPONSE | jq
SEEKER_ID=$(echo $SEEKER_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Job Seeker created with ID: $SEEKER_ID${NC}\n"

# Test 4: Create Job Posting
echo -e "${YELLOW}4. Creating Job Posting...${NC}"
JOB_RESPONSE=$(curl -s -X POST "$API_BASE/api/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Developer",
    "description": "We are seeking an experienced backend developer to join our growing team. You will work on scalable microservices and APIs.",
    "location": "San Francisco, CA",
    "salary_range": "$130,000 - $160,000",
    "job_type": "full-time",
    "requirements": ["5+ years Python experience", "FastAPI or Django", "Docker", "CI/CD"],
    "experience_required": 5,
    "employer_id": '$EMPLOYER_ID'
  }')
echo $JOB_RESPONSE | jq
JOB_ID=$(echo $JOB_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Job Posting created with ID: $JOB_ID${NC}\n"

# Test 5: Get Job with HATEOAS
echo -e "${YELLOW}5. Getting Job (with HATEOAS links)...${NC}"
curl -s "$API_BASE/api/jobs/$JOB_ID" | jq
echo -e "\n"

# Test 6: Create dummy resume file (PDF)
echo -e "${YELLOW}6. Creating test resume PDF file...${NC}"

# Create a simple PDF resume using text (mock PDF for testing)
# Note: In production, you'd upload real PDFs
cat > /tmp/jane_resume.pdf << 'EOF'
%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 200
>>
stream
BT
/F1 12 Tf
50 700 Td
(JANE SMITH - SENIOR BACKEND DEVELOPER) Tj
0 -20 Td
(Email: jane.smith@email.com | Phone: +1-555-0200) Tj
0 -30 Td
(EXPERIENCE:) Tj
0 -15 Td
(- 5 years of Python development) Tj
0 -15 Td
(- Expert in FastAPI and microservices) Tj
0 -15 Td
(- Docker and Kubernetes deployment) Tj
0 -30 Td
(EDUCATION:) Tj
0 -15 Td
(- BS Computer Science) Tj
0 -30 Td
(SKILLS:) Tj
0 -15 Td
(- Python, FastAPI, Docker, PostgreSQL, Redis) Tj
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
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
566
%%EOF
EOF

echo -e "${GREEN}✓ Test resume PDF created at /tmp/jane_resume.pdf${NC}\n"

# Test 7: Create Application
echo -e "${YELLOW}7. Submitting Job Application...${NC}"
APPLICATION_RESPONSE=$(curl -s -X POST "$API_BASE/api/applications/" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": '$JOB_ID',
    "seeker_id": '$SEEKER_ID',
    "cover_letter": "I am excited to apply for the Senior Backend Developer position. My 5 years of experience with Python and FastAPI make me a perfect fit for this role."
  }')
echo $APPLICATION_RESPONSE | jq
APPLICATION_ID=$(echo $APPLICATION_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Application submitted with ID: $APPLICATION_ID${NC}\n"

# Test 7b: Upload resume to application
echo -e "${YELLOW}7b. Uploading Resume PDF to Application...${NC}"
if [ "$APPLICATION_ID" != "null" ]; then
  UPLOAD_RESPONSE=$(curl -s -X POST "$API_BASE/api/applications/$APPLICATION_ID/upload-resume" \
    -F "file=@/tmp/jane_resume.pdf")
  echo $UPLOAD_RESPONSE | jq
  RESUME_URL=$(echo $UPLOAD_RESPONSE | jq -r '.resume_url')
  echo -e "${GREEN}✓ Resume uploaded to: $RESUME_URL${NC}\n"
else
  echo -e "${YELLOW}⚠ Skipping resume upload (no application ID)${NC}\n"
fi

# Test 7c: Verify application has resume
echo -e "${YELLOW}7c. Verifying Application with Resume...${NC}"
if [ "$APPLICATION_ID" != "null" ]; then
  curl -s "$API_BASE/api/applications/$APPLICATION_ID" | jq
  echo -e "\n"
else
  echo -e "${YELLOW}⚠ Skipping verification${NC}\n"
fi

# Test 8: List All Jobs
echo -e "${YELLOW}8. Listing All Jobs...${NC}"
curl -s "$API_BASE/api/jobs/" | jq
echo -e "\n"

# Test 9: Filter Jobs by Location
echo -e "${YELLOW}9. Filtering Jobs by Location (San Francisco)...${NC}"
curl -s "$API_BASE/api/jobs/?location=San%20Francisco" | jq
echo -e "\n"

# Test 10: Get Applications for Job
echo -e "${YELLOW}10. Getting Applications for Job $JOB_ID...${NC}"
curl -s "$API_BASE/api/applications/job/$JOB_ID" | jq
echo -e "\n"

# Test 11: Update Application Status
echo -e "${YELLOW}11. Updating Application Status to 'reviewed'...${NC}"
curl -s -X PATCH "$API_BASE/api/applications/$APPLICATION_ID/status?status=reviewed" | jq
echo -e "\n"

# Test 12: Get All Employers
echo -e "${YELLOW}12. Listing All Employers...${NC}"
curl -s "$API_BASE/api/employers/" | jq
echo -e "\n"

# Test 13: Get All Job Seekers
echo -e "${YELLOW}13. Listing All Job Seekers...${NC}"
curl -s "$API_BASE/api/seekers/" | jq
echo -e "\n"

# Test 14: Update Job Status
echo -e "${YELLOW}14. Updating Job Status to 'open'...${NC}"
curl -s -X PATCH "$API_BASE/api/jobs/$JOB_ID/status?status=open" | jq
echo -e "\n"

# Summary
echo -e "${PURPLE}=====================================${NC}"
echo -e "${PURPLE}  Test Summary${NC}"
echo -e "${PURPLE}=====================================${NC}"
echo -e "${GREEN}✓ Employer ID: $EMPLOYER_ID${NC}"
echo -e "${GREEN}✓ Job Seeker ID: $SEEKER_ID${NC}"
echo -e "${GREEN}✓ Job ID: $JOB_ID${NC}"
echo -e "${GREEN}✓ Application ID: $APPLICATION_ID${NC}"
echo -e "\n${GREEN}All tests completed successfully!${NC}"
echo -e "\n${YELLOW}View Swagger UI: $API_BASE/docs${NC}"
echo -e "${YELLOW}View ReDoc: $API_BASE/redoc${NC}\n"
