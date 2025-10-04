# 📂 Job Portal API - File Organization Guide

This guide helps you navigate the project structure and find what you need.

---

## 🗂️ Folder Structure

```
job-portal-api/
│
├── 📄 README.md                 ← Start here! Main project overview
├── 📄 Dockerfile                ← Container image configuration
├── 📄 docker-compose.yml        ← Docker orchestration
│
├── 📁 app/                      ← Application source code
│   ├── main.py                 ← FastAPI entry point
│   ├── models.py               ← Data models
│   ├── database.py             ← Database setup
│   ├── requirements.txt        ← Python dependencies
│   └── routes/                 ← API endpoints
│       ├── jobs.py
│       ├── employers.py
│       ├── seekers.py
│       └── applications.py
│
├── 📁 scripts/                  ← Utility scripts
│   ├── README.md               ← Scripts documentation
│   ├── demo.sh                 ← Quick demonstration
│   ├── test_api.sh             ← Test suite
│   └── inspect_db.sh           ← Database inspector
│
└── 📁 docs/                     ← Documentation
    ├── README.md               ← Documentation index
    ├── PROJECT_COMPLETE.md     ← Project status & details
    └── DATABASE_PERSISTENCE.md ← Storage guide
```

---

## 🎯 Where to Find What

### I want to...

**Get started quickly**
→ Read `README.md` (this folder)

**Understand what was implemented**
→ Read `docs/PROJECT_COMPLETE.md`

**Learn about data storage**
→ Read `docs/DATABASE_PERSISTENCE.md`

**Run a demo**
→ Execute `./scripts/demo.sh`

**Test the API**
→ Execute `./scripts/test_api.sh`

**Check database contents**
→ Execute `./scripts/inspect_db.sh`

**View API documentation**
→ Visit http://localhost:8000/docs

**Understand the scripts**
→ Read `scripts/README.md`

**See all documentation**
→ Read `docs/README.md`

**Modify the API**
→ Edit files in `app/` folder

**Configure Docker**
→ Edit `docker-compose.yml` or `Dockerfile`

---

## 📚 Documentation Files

| File                           | Purpose                        | When to Read                 |
| ------------------------------ | ------------------------------ | ---------------------------- |
| `README.md`                    | Project overview & quick start | First time, getting started  |
| `docs/PROJECT_COMPLETE.md`     | Complete project status        | Understanding implementation |
| `docs/DATABASE_PERSISTENCE.md` | Data storage details           | Managing database            |
| `docs/README.md`               | Documentation index            | Finding specific docs        |
| `scripts/README.md`            | Scripts usage guide            | Using utility scripts        |

---

## 🔧 Script Files

| Script                  | What it Does            | When to Use           |
| ----------------------- | ----------------------- | --------------------- |
| `scripts/demo.sh`       | Creates sample data     | Quick demonstration   |
| `scripts/test_api.sh`   | Tests all endpoints     | Comprehensive testing |
| `scripts/inspect_db.sh` | Shows database contents | Checking data         |

---

## 💻 Source Code Files

| File                         | Purpose                    |
| ---------------------------- | -------------------------- |
| `app/main.py`                | FastAPI application setup  |
| `app/models.py`              | Pydantic models & schemas  |
| `app/database.py`            | SQLite connection & tables |
| `app/requirements.txt`       | Python dependencies        |
| `app/routes/jobs.py`         | Job posting endpoints      |
| `app/routes/employers.py`    | Employer endpoints         |
| `app/routes/seekers.py`      | Job seeker endpoints       |
| `app/routes/applications.py` | Application endpoints      |

---

## 🚀 Quick Start Commands

```bash
# 1. Start the API
docker compose up -d --build
sleep 5

# 2. Run demo
./scripts/demo.sh

# 3. View API docs
open http://localhost:8000/docs  # or visit in browser

# 4. Inspect database
./scripts/inspect_db.sh

# 5. Run tests
./scripts/test_api.sh

# 6. Stop API
docker compose down
```

---

## 📖 Reading Order for New Users

1. **README.md** (5 min)

   - Get overview
   - Understand features
   - See quick start

2. **scripts/demo.sh** (1 min)

   - Run to see API in action
   - Creates sample data

3. **http://localhost:8000/docs** (10 min)

   - Explore API interactively
   - Try endpoints

4. **docs/PROJECT_COMPLETE.md** (15 min)

   - Understand full implementation
   - See what was completed
   - Review RESTful principles

5. **docs/DATABASE_PERSISTENCE.md** (10 min)
   - Learn about data storage
   - Understand persistence

---

## 🎓 For Assignment Reviewers

### Essential Files to Review:

1. **README.md** - Project overview
2. **docs/PROJECT_COMPLETE.md** - Implementation details
3. **app/main.py** - API setup
4. **app/routes/\*.py** - Endpoint implementations
5. **http://localhost:8000/docs** - Live API documentation

### Quick Verification:

```bash
# Start API
docker compose up -d --build && sleep 5

# Run demo (creates test data)
./scripts/demo.sh

# Verify it works
curl http://localhost:8000/api/jobs/ | jq

# Check database
./scripts/inspect_db.sh
```

---

## 🗺️ Navigation Tips

### From Root Directory:

```bash
# View main README
cat README.md

# View project status
cat docs/PROJECT_COMPLETE.md

# View database docs
cat docs/DATABASE_PERSISTENCE.md

# Run demo
./scripts/demo.sh

# Run tests
./scripts/test_api.sh
```

### Useful Shortcuts:

```bash
# View all documentation
ls -la docs/

# View all scripts
ls -la scripts/

# View all routes
ls -la app/routes/

# Check running containers
docker compose ps

# View logs
docker compose logs -f jobapi
```

---

## 🔍 File Finding Commands

```bash
# Find all Python files
find . -name "*.py"

# Find all markdown files
find . -name "*.md"

# Find all shell scripts
find . -name "*.sh"

# Search for text in files
grep -r "HATEOAS" .

# Show project tree
tree -L 2
```

---

## 📊 Project Statistics

- **Total Files**: 20+
- **Documentation Files**: 5 (README files + guides)
- **Python Files**: 9 (main app + routes)
- **Scripts**: 3 (demo, test, inspect)
- **Configuration Files**: 2 (Dockerfile, docker-compose)
- **Total Lines of Code**: ~3000+
- **Total Documentation Lines**: ~2000+

---

## ✅ File Checklist

Use this to ensure you have all files:

### Root Level

- [ ] README.md
- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] .dockerignore

### App Folder

- [ ] app/main.py
- [ ] app/models.py
- [ ] app/database.py
- [ ] app/requirements.txt
- [ ] app/routes/jobs.py
- [ ] app/routes/employers.py
- [ ] app/routes/seekers.py
- [ ] app/routes/applications.py

### Scripts Folder

- [ ] scripts/README.md
- [ ] scripts/demo.sh
- [ ] scripts/test_api.sh
- [ ] scripts/inspect_db.sh

### Docs Folder

- [ ] docs/README.md
- [ ] docs/PROJECT_COMPLETE.md
- [ ] docs/DATABASE_PERSISTENCE.md

---

## 🎯 Quick Reference

| I need...              | Go to...                       |
| ---------------------- | ------------------------------ |
| Project overview       | `README.md`                    |
| Implementation details | `docs/PROJECT_COMPLETE.md`     |
| Storage info           | `docs/DATABASE_PERSISTENCE.md` |
| Run demo               | `./scripts/demo.sh`            |
| Run tests              | `./scripts/test_api.sh`        |
| Check database         | `./scripts/inspect_db.sh`      |
| API docs               | http://localhost:8000/docs     |
| Modify endpoints       | `app/routes/*.py`              |
| Change models          | `app/models.py`                |
| Database setup         | `app/database.py`              |

---

**Last Updated**: October 4, 2025  
**Project Status**: ✅ Complete and Ready
