#!/bin/bash

# Quick API Demo - Job Portal Platform
# Demonstrates the complete workflow

API_BASE="http://localhost:8000"

echo "=========================================="
echo "   Job Portal API - Quick Demo"
echo "=========================================="
echo ""

# Use timestamp to make unique emails
TIMESTAMP=$(date +%s)

echo "1️⃣  Creating Employer..."
EMPLOYER=$(curl -s -X POST "$API_BASE/api/employers/" \
  -H "Content-Type: application/json" \
  -d "{
    \"company_name\": \"TechStart $TIMESTAMP\",
    \"email\": \"hr$TIMESTAMP@techstart.com\",
    \"phone\": \"+1-555-0100\",
    \"description\": \"Innovative startup building the future\",
    \"website\": \"https://techstart.com\"
  }")

EMPLOYER_ID=$(echo $EMPLOYER | jq -r '.id')
echo "   ✓ Created Employer (ID: $EMPLOYER_ID)"
echo ""

echo "2️⃣  Creating Job Seeker..."
SEEKER=$(curl -s -X POST "$API_BASE/api/seekers/" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Alex Johnson\",
    \"email\": \"alex$TIMESTAMP@email.com\",
    \"phone\": \"+1-555-0200\",
    \"skills\": [\"Python\", \"FastAPI\", \"Docker\"],
    \"experience_years\": 3
  }")

SEEKER_ID=$(echo $SEEKER | jq -r '.id')
echo "   ✓ Created Job Seeker (ID: $SEEKER_ID)"
echo ""

echo "3️⃣  Posting a Job..."
JOB=$(curl -s -X POST "$API_BASE/api/jobs/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Python Developer\",
    \"description\": \"Build amazing APIs\",
    \"location\": \"Remote\",
    \"salary_range\": \"\$80k-\$120k\",
    \"job_type\": \"full-time\",
    \"requirements\": [\"Python\", \"FastAPI\"],
    \"experience_required\": 2,
    \"employer_id\": $EMPLOYER_ID
  }")

JOB_ID=$(echo $JOB | jq -r '.id')
echo "   ✓ Created Job Posting (ID: $JOB_ID)"
echo ""

echo "4️⃣  Getting Job with HATEOAS Links..."
curl -s "$API_BASE/api/jobs/$JOB_ID" | jq '.links'
echo ""

echo "5️⃣  Submitting Application..."
APP=$(curl -s -X POST "$API_BASE/api/applications/" \
  -H "Content-Type: application/json" \
  -d "{
    \"job_id\": $JOB_ID,
    \"seeker_id\": $SEEKER_ID,
    \"cover_letter\": \"I'm excited to apply for this position!\"
  }")

APP_ID=$(echo $APP | jq -r '.id')
echo "   ✓ Submitted Application (ID: $APP_ID)"
echo ""

echo "5️⃣b Uploading Resume to Application..."
# Create a simple PDF resume for demo
cat > /tmp/demo_resume_${TIMESTAMP}.pdf << 'EOF'
%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>>>endobj
4 0 obj<</Length 150>>stream
BT
/F1 14 Tf
50 700 Td
(ALEX JOHNSON - RESUME) Tj
0 -30 Td
(Python Developer with 3 years experience) Tj
0 -20 Td
(Skills: Python, FastAPI, Docker) Tj
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

UPLOAD_RESULT=$(curl -s -X POST "$API_BASE/api/applications/$APP_ID/upload-resume" \
  -F "file=@/tmp/demo_resume_${TIMESTAMP}.pdf")
RESUME_URL=$(echo $UPLOAD_RESULT | jq -r '.access_url')
echo "   ✓ Resume uploaded: $RESUME_URL"
rm -f /tmp/demo_resume_${TIMESTAMP}.pdf
echo ""

echo "6️⃣  Listing All Jobs..."
curl -s "$API_BASE/api/jobs/" | jq 'length'
echo "   jobs found"
echo ""

echo "7️⃣  Getting Applications for Job..."
curl -s "$API_BASE/api/applications/job/$JOB_ID" | jq 'length'
echo "   applications found"
echo ""

echo "=========================================="
echo "✅ Demo completed successfully!"
echo ""
echo "📖 View full API docs: $API_BASE/docs"
echo "=========================================="
