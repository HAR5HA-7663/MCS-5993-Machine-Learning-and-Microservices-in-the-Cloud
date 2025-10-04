#!/bin/bash

echo "🌱 Seeding database with sample cars..."
echo ""

# Get the first backend pod
BACKEND_POD=$(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}')

if [ -z "$BACKEND_POD" ]; then
    echo "❌ Error: No backend pod found!"
    echo "Make sure the application is running: kubectl get pods"
    exit 1
fi

echo "Using backend pod: $BACKEND_POD"
echo ""

kubectl exec -it "$BACKEND_POD" -- python seed_data.py

echo ""
echo "✅ Database seeding complete!"
echo "Access your app at: http://localhost:30080"
