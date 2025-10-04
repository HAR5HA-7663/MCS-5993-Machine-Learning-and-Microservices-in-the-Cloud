#!/bin/bash

echo "🚀 Starting Car Dealer App..."
echo ""

# Get the project root directory (parent of k8s)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Step 1: Building Docker images..."
cd "$PROJECT_ROOT"
docker compose build

echo ""
echo "Step 2: Deploying to Kubernetes..."
kubectl apply -f k8s/

echo ""
echo "Step 3: Waiting for pods to be ready..."
echo "Press Ctrl+C when all pods show READY 1/1"
echo ""
kubectl get pods -w
