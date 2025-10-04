# Scripts Directory

This folder contains utility scripts for testing, demonstrating, and managing the Job Portal API.

---

## 📜 Available Scripts

### 1. `demo.sh` - Quick API Demonstration

**Purpose**: Demonstrates the complete workflow of the Job Portal API by creating sample data.

**What it does**:

- Creates an employer profile
- Creates a job seeker profile
- Posts a job listing
- Submits a job application
- Shows HATEOAS links
- Lists all data

**Usage**:

```bash
./scripts/demo.sh
```

**Expected Output**:

```
==========================================
   Job Portal API - Quick Demo
==========================================

1️⃣  Creating Employer...
   ✓ Created Employer (ID: X)

2️⃣  Creating Job Seeker...
   ✓ Created Job Seeker (ID: X)

3️⃣  Posting a Job...
   ✓ Created Job Posting (ID: X)

4️⃣  Getting Job with HATEOAS Links...
   {HATEOAS links displayed}

5️⃣  Submitting Application...
   ✓ Submitted Application (ID: X)

✅ Demo completed successfully!
```

---

### 2. `test_api.sh` - Comprehensive API Test Suite

**Purpose**: Tests all major API endpoints with various scenarios.

**What it does**:

- Tests root endpoint
- Creates employers, seekers, jobs, applications
- Tests filtering by location
- Tests status updates
- Lists all resources
- Validates HATEOAS implementation

**Usage**:

```bash
./scripts/test_api.sh
```

**Features**:

- ✅ Tests all CRUD operations
- ✅ Validates response formats
- ✅ Tests query parameters
- ✅ Verifies HATEOAS links
- ✅ Tests file uploads
- ✅ Color-coded output

**Output**: Detailed test results for 14+ test cases

---

### 3. `inspect_db.sh` - Database Inspector

**Purpose**: View the contents of the SQLite database without accessing the container.

**What it does**:

- Connects to the database inside the Docker container
- Displays all data from each table
- Shows summary statistics
- Provides instructions for direct access

**Usage**:

```bash
./scripts/inspect_db.sh
```

**Expected Output**:

```
==========================================
   Job Portal Database Inspector
==========================================

📊 Database Location: Inside Docker volume 'job-portal-api_db_data'
   Path inside container: /app/data/jobportal.db

📋 Tables and Data:

👔 EMPLOYERS:
1 | TechStart 1759595176 | hr1759595176@techstart.com

👤 JOB SEEKERS:
1 | Alex Johnson | alex1759595176@email.com | 3 years

💼 JOB POSTINGS:
1 | Python Developer | Remote | full-time | open

📝 APPLICATIONS:
1 | Job #1 | Seeker #1 | pending

📊 Summary:
   Employers: 1
   Job Seekers: 1
   Job Postings: 1
   Applications: 1
```

---

## 🚀 Quick Start

### First Time Setup

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start the API
docker compose up -d --build

# Wait for API to start (3-5 seconds)
sleep 5

# Run demo
./scripts/demo.sh
```

### Testing the API

```bash
# Run comprehensive tests
./scripts/test_api.sh

# Inspect database
./scripts/inspect_db.sh
```

---

## 🔧 Script Requirements

All scripts require:

- ✅ Docker and Docker Compose installed
- ✅ API running on `http://localhost:8000`
- ✅ `curl` and `jq` installed (for JSON parsing)
- ✅ Bash shell

### Install Dependencies (if needed)

```bash
# Ubuntu/Debian
sudo apt-get install curl jq

# macOS
brew install curl jq

# Fedora
sudo dnf install curl jq
```

---

## 📝 Script Descriptions

| Script          | Purpose         | Use Case               | Duration   |
| --------------- | --------------- | ---------------------- | ---------- |
| `demo.sh`       | Quick demo      | Show API capabilities  | ~2 seconds |
| `test_api.sh`   | Full test suite | Validate all endpoints | ~5 seconds |
| `inspect_db.sh` | Database viewer | Check stored data      | ~1 second  |

---

## 🎯 Common Workflows

### Workflow 1: Initial Setup & Demo

```bash
docker compose up -d --build
sleep 5
./scripts/demo.sh
```

### Workflow 2: Full Testing

```bash
./scripts/test_api.sh
./scripts/inspect_db.sh
```

### Workflow 3: Check Data After Restart

```bash
docker compose restart jobapi
sleep 3
./scripts/inspect_db.sh
```

### Workflow 4: Fresh Start

```bash
docker compose down -v
docker compose up -d --build
sleep 5
./scripts/demo.sh
```

---

## 🐛 Troubleshooting

### Script Not Executable

```bash
chmod +x scripts/demo.sh
chmod +x scripts/test_api.sh
chmod +x scripts/inspect_db.sh
```

### API Not Running

```bash
docker compose ps
# If not running:
docker compose up -d
sleep 5
```

### Connection Refused

```bash
# Check if API is ready
curl http://localhost:8000/
# Wait a few more seconds if it fails
```

### jq Command Not Found

```bash
# Install jq
sudo apt-get install jq  # Ubuntu/Debian
brew install jq          # macOS
```

---

## 🔄 Script Maintenance

### Adding New Scripts

1. Create script in `scripts/` folder
2. Make it executable: `chmod +x scripts/your_script.sh`
3. Add description to this README
4. Test thoroughly

### Best Practices

- ✅ Use absolute paths or cd to project root
- ✅ Check if API is running before making requests
- ✅ Add error handling
- ✅ Provide clear output messages
- ✅ Use colors for better readability

---

## 📖 API Endpoints Reference

For complete API documentation, see:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Main README: `../README.md`

---

## 🤝 Contributing

When adding new scripts:

1. Follow the existing naming convention
2. Add comprehensive comments
3. Update this README
4. Test on clean installation

---

**Last Updated**: October 4, 2025
