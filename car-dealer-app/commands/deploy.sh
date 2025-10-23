#!/bin/bash

# Deploy using pre-built images
echo "🚀 Deploying Vroomm Vrommmm with pre-built images..."

# Use production docker-compose with pre-built images
docker compose -f docker-compose.prod.yml up -d

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Frontend: http://localhost:8080"
    echo "🔧 Backend API: http://localhost:5000"
    echo ""
    echo "To seed the database:"
    echo "  docker compose -f docker-compose.prod.yml run backend python seed_data.py"
    echo ""
    echo "To stop: docker compose -f docker-compose.prod.yml down"
else
    echo "❌ Deployment failed"
    exit 1
fi