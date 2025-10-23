#!/bin/bash

# Complete cleanup script - removes everything including volumes
echo "🧹 Performing complete cleanup of Vroomm Vrommmm Car Dealer App..."
echo "⚠️  This will remove all data including the database!"

read -p "Are you sure? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Stop and remove everything including volumes
    docker compose down --volumes --remove-orphans
    
    # Remove custom images
    echo "Removing custom images..."
    docker rmi car-dealer-app-frontend car-dealer-app-backend 2>/dev/null || true
    
    echo "✅ Complete cleanup finished!"
else
    echo "❌ Cleanup cancelled"
fi