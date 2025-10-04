# 🚗 Vroomm Vrommmm Car Dealer Management System

A modern, full-stack car dealership inventory management system built with Flask, PostgreSQL, Nginx, and deployed on Kubernetes.

## 🎯 Features

- ➕ **Add New Cars** - Add vehicles to inventory with VIN, year, brand, model, mileage, and price
- 📊 **Sort & Filter** - Sort by year, brand, model, price, mileage, or date added
- 🗑️ **Bulk Delete** - Select multiple cars and delete with confirmation
- 📅 **Timestamp Tracking** - Automatically track when each car was added
- 🎨 **Modern UI** - Beautiful, responsive design with gradients and animations
- 📱 **Mobile Responsive** - Works perfectly on all devices

## 🏗️ Architecture

- **Frontend**: Nginx serving static HTML/CSS/JavaScript
- **Backend**: Flask REST API with CORS support
- **Database**: PostgreSQL with persistent storage
- **Orchestration**: Kubernetes with 2 replicas for high availability
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
car-dealer-app/
├── backend/              # Flask API
│   ├── app.py           # Main application
│   ├── seed_data.py     # Database seeding script
│   ├── migrate_db.py    # Database migration script
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container
├── frontend/            # Nginx web server
│   ├── index.html      # Main UI
│   ├── style.css       # Modern styling
│   ├── nginx.conf      # Nginx configuration
│   └── Dockerfile      # Frontend container
├── k8s/                # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── web-deployment.yaml
│   ├── web-service.yaml
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── postgres-pvc.yaml
│   └── README.md
├── commands/           # ⭐ Management scripts
│   ├── README.md       # Complete command reference
│   ├── start.sh        # Start everything
│   ├── stop.sh         # Stop everything
│   ├── restart.sh      # Full restart
│   └── seed-db.sh      # Seed database
└── docker-compose.yml  # Docker Compose config

```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop with Kubernetes enabled
- kubectl configured
- Linux/Mac/WSL environment

### 1. Clone and Navigate

```bash
cd /media/har5ha/HDD/Desktop/labs/car-dealer-app
```

### 2. Start the Application

```bash
./commands/start.sh
```

### 3. Seed the Database

```bash
./commands/seed-db.sh
```

### 4. Access the Application

Open your browser to: **http://localhost:30080**

## 📚 Management Commands

All management scripts are in the `commands/` folder:

```bash
# Start everything (build + deploy)
./commands/start.sh

# Stop everything (delete all resources)
./commands/stop.sh

# Full restart (stop + rebuild + start)
./commands/restart.sh

# Seed database with 50 sample cars
./commands/seed-db.sh
```

**📖 For complete documentation, see: [`commands/README.md`](commands/README.md)**

## 🛠️ Development

### Making Frontend Changes

```bash
# Edit files in frontend/
docker compose build frontend
kubectl rollout restart deployment web-deployment
# Hard refresh browser: Ctrl+Shift+R
```

### Making Backend Changes

```bash
# Edit files in backend/
docker compose build backend
kubectl rollout restart deployment backend-deployment
kubectl logs -l app=backend -f
```

### Checking Status

```bash
kubectl get pods          # Check pod status
kubectl get svc           # Check services
kubectl logs -l app=backend -f   # View backend logs
```

## 📊 API Endpoints

- `GET /api/cars?page=1&sort_by=year&sort_order=DESC` - Get paginated, sorted cars
- `POST /api/cars` - Add new car
- `DELETE /api/cars` - Delete multiple cars by VINs
- `GET /api/health` - Health check

## 🎨 Tech Stack

**Frontend:**

- HTML5, CSS3 (Modern design with CSS variables)
- Vanilla JavaScript (Fetch API)
- Nginx (Web server)

**Backend:**

- Python 3.12
- Flask (REST API)
- Flask-CORS (Cross-origin support)
- psycopg2 (PostgreSQL driver)

**Database:**

- PostgreSQL 16 Alpine
- Persistent volume for data storage

**DevOps:**

- Docker & Docker Compose
- Kubernetes (deployments, services, PVC)
- Docker Desktop Kubernetes

## 🔧 Configuration

### Environment Variables (Backend)

- `DATABASE_URL`: PostgreSQL connection string
  - Default: `postgres://caruser:carpass@db-service:5432/cardb`

### Ports

- **Frontend**: 30080 (NodePort)
- **Backend**: 5000 (ClusterIP)
- **Database**: 5432 (ClusterIP)

## 📝 Database Schema

```sql
CREATE TABLE cars (
    vin VARCHAR(20) PRIMARY KEY,
    year INT,
    brand TEXT,
    model TEXT,
    mileage INT,
    price INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🐛 Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### CSS Not Loading

```bash
# Rebuild and restart frontend
docker compose build frontend
kubectl rollout restart deployment web-deployment
# Hard refresh: Ctrl+Shift+R
```

### Database Issues

```bash
# Check database pod
kubectl logs -l app=db

# Reseed database
./commands/seed-db.sh
```

**For more troubleshooting, see: [`commands/README.md`](commands/README.md)**

## 📦 Kubernetes Resources

- **Deployments**: 3 (db, backend, web)
- **Services**: 3 (ClusterIP for db & backend, NodePort for web)
- **PVC**: 1 (postgres-pvc for database persistence)
- **Replicas**: 1 (db), 2 (backend), 2 (web)

## 🌟 Features in Detail

### Add Car

- Form validation
- Duplicate VIN detection
- Success/error messages
- Automatic timestamp

### Sort & Filter

- Sort by: Year, Brand, Model, Price, Mileage, Date Added
- Ascending/Descending order
- Instant results

### Delete Cars

- Multi-select with checkboxes
- Select all option
- Confirmation dialog
- Batch deletion

## 🤝 Contributing

This is a learning project for Kubernetes deployment practice.

## 📄 License

MIT License - Feel free to use for learning!

## 🎓 Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Support

For detailed commands and troubleshooting, always refer to:
👉 **[`commands/README.md`](commands/README.md)**

---

**Built with ❤️ for learning Kubernetes deployments**

🚗 Happy Car Dealing! 🚗
