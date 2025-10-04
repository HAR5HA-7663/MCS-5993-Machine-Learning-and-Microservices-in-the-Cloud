#!/bin/bash

echo "🛑 Stopping all Kubernetes resources..."
echo ""

echo "Deleting deployments, services, and pods..."
kubectl delete all --all

echo ""
echo "Deleting persistent volume claims..."
kubectl delete pvc --all

echo ""
echo "✅ All resources deleted!"
echo ""
echo "To verify deletion, run: kubectl get all"
echo "To start again, run: ./start.sh"
