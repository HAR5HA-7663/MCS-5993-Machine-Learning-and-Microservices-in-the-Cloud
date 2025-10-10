# 🏗️ BUILD & DEPLOY (for your assignment)

./build-k8s.sh # Build Docker images
kubectl apply -f k8s/ # Deploy to Kubernetes  
kubectl get pods -w # Watch deployment

# 🌐 ACCESS APPLICATION

http://localhost:30080 # Frontend
http://localhost:30080/api/cars # Backend API

# 🔍 MONITOR & DEBUG

kubectl get all # Check all resources
kubectl logs -l app=backend -f # Backend logs
kubectl logs -l app=web -f # Frontend logs

# 🗄️ SEED DATABASE

kubectl get pods -l app=backend # Get backend pod name
kubectl exec -it <pod-name> -- python seed_data.py

# 🛑 STOP EVERYTHING

kubectl delete all --all && kubectl delete pvc --all
