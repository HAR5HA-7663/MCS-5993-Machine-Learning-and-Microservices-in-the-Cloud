#!/bin/bash

echo "🧹 Deep cleaning local Docker environment..."
echo ""

echo "Stopping all Kubernetes resources..."
kubectl delete all --all 2>/dev/null
kubectl delete pvc --all 2>/dev/null

echo ""
echo "Removing Docker images (keeping system images)..."
docker rmi $(docker images --filter "reference=car-dealer-app*" -q) 2>/dev/null
docker rmi $(docker images --filter "reference=postgres:16-alpine" -q) 2>/dev/null

echo ""  
echo "Cleaning up Docker system..."
docker system prune -a -f
docker volume prune -f

echo ""
echo "✅ Local cleanup complete!"
echo "💾 Kubernetes files preserved for your assignment"