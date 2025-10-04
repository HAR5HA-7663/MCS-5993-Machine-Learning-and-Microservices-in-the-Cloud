#!/bin/bash

echo "🔄 Restarting Car Dealer App..."
echo ""

# Get the project root directory (parent of k8s)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Step 1: Deleting old resources..."
kubectl delete all --all
kubectl delete pvc --all

echo ""
echo "Step 2: Waiting for cleanup..."
sleep 5

echo ""
echo "Step 3: Rebuilding Docker images..."
cd "$PROJECT_ROOT"
docker compose build

echo ""
echo "Step 4: Deploying to Kubernetes..."
kubectl apply -f k8s/

echo ""
echo "Step 5: Waiting for pods to be ready..."
echo "Press Ctrl+C when all pods show READY 1/1"
echo ""
kubectl get pods -w
