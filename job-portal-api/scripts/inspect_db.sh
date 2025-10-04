#!/bin/bash

echo "=========================================="
echo "   Job Portal Database Inspector"
echo "=========================================="
echo ""

echo "📊 Database Location: Inside Docker volume 'job-portal-api_db_data'"
echo "   Path inside container: /app/data/jobportal.db"
echo ""

echo "📋 Tables and Data:"
echo ""

echo "👔 EMPLOYERS:"
docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT id, company_name, email FROM employers'); [print(f'{row[0]} | {row[1]} | {row[2]}') for row in cursor.fetchall()]; conn.close()" 2>/dev/null
echo ""

echo "👤 JOB SEEKERS:"
docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT id, name, email, experience_years FROM job_seekers'); [print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} years') for row in cursor.fetchall()]; conn.close()" 2>/dev/null
echo ""

echo "💼 JOB POSTINGS:"
docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT id, title, location, job_type, status FROM job_postings'); [print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}') for row in cursor.fetchall()]; conn.close()" 2>/dev/null
echo ""

echo "📝 APPLICATIONS:"
docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT id, job_id, seeker_id, status FROM applications'); [print(f'{row[0]} | Job #{row[1]} | Seeker #{row[2]} | {row[3]}') for row in cursor.fetchall()]; conn.close()" 2>/dev/null
echo ""

echo "=========================================="
echo "📊 Summary:"
EMPLOYERS=$(docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM employers'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null)
SEEKERS=$(docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM job_seekers'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null)
JOBS=$(docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM job_postings'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null)
APPS=$(docker exec job-portal-api python -c "import sqlite3; conn = sqlite3.connect('/app/data/jobportal.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM applications'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null)

echo "   Employers: $EMPLOYERS"
echo "   Job Seekers: $SEEKERS"
echo "   Job Postings: $JOBS"
echo "   Applications: $APPS"
echo "=========================================="
echo ""
echo "💡 To access database directly using Python:"
echo "   docker exec -it job-portal-api python"
echo "   >>> import sqlite3"
echo "   >>> conn = sqlite3.connect('/app/data/jobportal.db')"
echo "   >>> cursor = conn.cursor()"
echo "   >>> cursor.execute('SELECT * FROM employers')"
echo "   >>> cursor.fetchall()"
echo ""
