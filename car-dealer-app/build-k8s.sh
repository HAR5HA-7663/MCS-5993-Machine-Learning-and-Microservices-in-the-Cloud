#!/bin/bash

echo "🏗️  Building Docker images for Kubernetes deployment..."
echo ""

# Build backend image
echo "Building backend..."
docker build -t car-dealer-app-backend:latest ./backend/

# Build frontend image for Kubernetes
echo "Building frontend..."
docker build -f ./frontend/Dockerfile.k8s -t car-dealer-app-frontend:latest ./frontend/

echo ""
echo "✅ Images built successfully!"
echo "🚀 Ready to deploy to Kubernetes:"
echo ""
echo "   kubectl apply -f k8s/"
echo "   kubectl get pods -w"
echo ""
echo "📱 Access app at: http://localhost:30080"