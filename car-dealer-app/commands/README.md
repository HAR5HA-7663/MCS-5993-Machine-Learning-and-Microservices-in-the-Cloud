# 🚀 Kubernetes Management Commands

## 🛑 Stop Everything (Delete All Resources)

### Option 1: Delete All Deployments, Services, and PVCs
```bash
# Delete all resources in one command
kubectl delete -f k8s/

# Or delete individually
kubectl delete deployment --all
kubectl delete service --all
kubectl delete pvc --all
```

### Option 2: Delete Everything in Default Namespace
```bash
# Delete all pods (will be recreated by deployments)
kubectl delete pods --all

# Delete all resources (deployments, services, pods, pvc)
kubectl delete all --all

# Delete PVCs separately (not included in 'all')
kubectl delete pvc --all
```

### Option 3: Nuclear Option (Complete Cleanup)
```bash
# Delete everything including configmaps, secrets, etc.
kubectl delete all --all
kubectl delete pvc --all
kubectl delete configmap --all
kubectl delete secret --all
```

---

## ✅ Verify Everything is Deleted
```bash
# Check all resources
kubectl get all

# Check PVCs
kubectl get pvc

# Should show: "No resources found in default namespace."
```

---

## 🚀 Start Everything Again (Full Deployment)

### Step 1: Build Docker Images (if needed)
```bash
# Navigate to project root
cd /media/har5ha/HDD/Desktop/labs/car-dealer-app

# Build all images
docker compose build

# Or build individually
docker compose build backend
docker compose build frontend
```

### Step 2: Deploy to Kubernetes
```bash
# Deploy everything in correct order
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/web-deployment.yaml
kubectl apply -f k8s/web-service.yaml

# Or deploy all at once
kubectl apply -f k8s/
```

### Step 3: Wait for Pods to be Ready
```bash
# Watch pods until all are running
kubectl get pods -w

# Or check status
kubectl get pods
```

### Step 4: Seed Database (Optional)
```bash
# Get backend pod name
kubectl get pods -l app=backend

# Seed the database (replace <backend-pod-name> with actual name)
kubectl exec -it <backend-pod-name> -- python seed_data.py

# Example:
kubectl exec -it backend-deployment-7cc6fffcbf-abc12 -- python seed_data.py
```

### Step 5: Access Application
```bash
# Open in browser
http://localhost:30080

# Or check service
kubectl get svc web-service
```

---

## 🔄 Quick Commands

### Restart Specific Deployment
```bash
# Restart backend
kubectl rollout restart deployment backend-deployment

# Restart frontend
kubectl rollout restart deployment web-deployment

# Restart database (careful - may lose data!)
kubectl rollout restart deployment db-deployment

# Restart all
kubectl rollout restart deployment backend-deployment web-deployment
```

### Scale Replicas
```bash
# Scale backend to 3 replicas
kubectl scale deployment backend-deployment --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment web-deployment --replicas=3

# Scale down to 1
kubectl scale deployment backend-deployment --replicas=1
```

### View Logs
```bash
# Backend logs (follow)
kubectl logs -l app=backend -f

# Frontend logs (follow)
kubectl logs -l app=web -f

# Database logs (follow)
kubectl logs -l app=db -f

# Specific pod logs
kubectl logs <pod-name> -f

# Last 50 lines
kubectl logs <pod-name> --tail=50
```

### Check Status
```bash
# All resources
kubectl get all

# Just pods
kubectl get pods

# Just services
kubectl get svc

# Detailed pod info
kubectl describe pod <pod-name>

# Wide output with node info
kubectl get pods -o wide
```

---

## 🔧 Troubleshooting

### Pod Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Image Pull Error
```bash
# Make sure images are built
docker images | grep car-dealer-app

# Rebuild if needed
cd /media/har5ha/HDD/Desktop/labs/car-dealer-app
docker compose build

# Check if images exist locally
docker images
```

### Database Connection Issues
```bash
# Check if db service is running
kubectl get svc db-service

# Check db pod logs
kubectl logs -l app=db

# Get into backend pod to test
kubectl exec -it <backend-pod-name> -- /bin/bash
```

### CSS Not Loading
```bash
# Rebuild frontend
docker compose build frontend

# Restart web deployment
kubectl rollout restart deployment web-deployment

# Hard refresh browser: Ctrl + Shift + R
```

### Clear Browser Cache
- **Chrome/Edge**: `Ctrl + Shift + R` or `Ctrl + F5`
- **Firefox**: `Ctrl + Shift + R`
- **Or**: Open DevTools (F12) → Network tab → Disable cache

---

## 📋 One-Liner Commands

### Stop Everything
```bash
kubectl delete all --all && kubectl delete pvc --all
```

### Start Everything (after images are built)
```bash
kubectl apply -f k8s/ && kubectl get pods -w
```

### Restart All Deployments
```bash
kubectl rollout restart deployment backend-deployment web-deployment
```

### Full Reset (Stop + Rebuild + Start)
```bash
cd /media/har5ha/HDD/Desktop/labs/car-dealer-app && kubectl delete all --all && kubectl delete pvc --all && sleep 5 && docker compose build && kubectl apply -f k8s/ && kubectl get pods -w
```

### Quick Restart (No Rebuild)
```bash
kubectl delete all --all && kubectl delete pvc --all && sleep 5 && kubectl apply -f k8s/
```

---

## 🎯 Quick Reference Table

| Action | Command |
|--------|---------|
| **Stop all** | `kubectl delete all --all && kubectl delete pvc --all` |
| **Start all** | `kubectl apply -f k8s/` |
| **Check status** | `kubectl get pods` |
| **View logs** | `kubectl logs -l app=backend -f` |
| **Restart** | `kubectl rollout restart deployment <name>` |
| **Scale** | `kubectl scale deployment <name> --replicas=<n>` |
| **Access app** | `http://localhost:30080` |
| **Seed DB** | `kubectl exec -it <backend-pod> -- python seed_data.py` |
| **Rebuild images** | `docker compose build` |
| **Get pod shell** | `kubectl exec -it <pod-name> -- /bin/bash` |

---

## 🌐 Application URLs

- **Frontend**: http://localhost:30080
- **Backend API**: http://localhost:30080/api/cars
- **Backend Health**: http://localhost:30080/api/health
- **Database**: Internal only (accessible via backend pods)

---

## 📝 Common Workflows

### Making Code Changes to Frontend
```bash
# 1. Edit files in frontend/
# 2. Rebuild image
docker compose build frontend

# 3. Restart deployment
kubectl rollout restart deployment web-deployment

# 4. Wait and hard refresh browser
kubectl get pods -w
# Then Ctrl+Shift+R in browser
```

### Making Code Changes to Backend
```bash
# 1. Edit files in backend/
# 2. Rebuild image
docker compose build backend

# 3. Restart deployment
kubectl rollout restart deployment backend-deployment

# 4. Check logs
kubectl logs -l app=backend -f
```

### Resetting Database
```bash
# 1. Get backend pod name
kubectl get pods -l app=backend

# 2. Run seed script (will clear and repopulate)
kubectl exec -it <backend-pod-name> -- python seed_data.py
```

### Checking Application Health
```bash
# Check all pods are running
kubectl get pods

# Check backend health endpoint
curl http://localhost:30080/api/health

# Check if you can get cars
curl http://localhost:30080/api/cars?page=1
```

---

## ⚠️ Important Notes

- **Data Persistence**: Database data is stored in PVC, survives pod restarts but NOT `kubectl delete pvc --all`
- **Images**: Uses local Docker images (Docker Desktop shares daemon with k8s)
- **Namespace**: All resources deployed to `default` namespace
- **Port**: Frontend exposed on NodePort 30080
- **Image Pull Policy**: Set to `IfNotPresent` - uses local images first
- **Cache**: Browser caching can cause issues - always hard refresh after redeployment

---

## 🆘 Emergency Commands

### Everything is Broken - Full Reset
```bash
cd /media/har5ha/HDD/Desktop/labs/car-dealer-app
kubectl delete all --all
kubectl delete pvc --all
sleep 10
docker compose build
kubectl apply -f k8s/
kubectl get pods -w
```

### Check What's Wrong
```bash
# Get all events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check all pod statuses
kubectl get pods -o wide

# Describe failing pod
kubectl describe pod <pod-name>

# Get logs from crashed pod
kubectl logs <pod-name> --previous
```

### Access Pod Shell for Debugging
```bash
# Backend pod
kubectl exec -it <backend-pod-name> -- /bin/bash

# Then inside pod:
ls -la
python seed_data.py
env | grep DATABASE
```

---

## 🎓 Learning Commands

### Understanding Your Deployment
```bash
# See all resources with labels
kubectl get all --show-labels

# See resource usage
kubectl top pods

# See which node pods are on
kubectl get pods -o wide

# Get deployment details
kubectl describe deployment backend-deployment

# See service endpoints
kubectl get endpoints
```

---

**Happy deploying! 🚀**

For more help: `kubectl --help` or visit https://kubernetes.io/docs/
