#!/bin/bash

# Build Docker Images Script for Vroomm Vrommmm Car Dealer App
echo "🐳 Building Docker Images for Vroomm Vrommmm Car Dealer App..."

# Set image tags with version
VERSION=${1:-latest}
REGISTRY=${2:-local}

if [ "$REGISTRY" != "local" ]; then
    FRONTEND_IMAGE="$REGISTRY/vroomm-frontend:$VERSION"
    BACKEND_IMAGE="$REGISTRY/vroomm-backend:$VERSION"
else
    FRONTEND_IMAGE="vroomm-frontend:$VERSION"
    BACKEND_IMAGE="vroomm-backend:$VERSION"
fi

echo "Building images with version: $VERSION"
echo "Registry: $REGISTRY"

# Build backend image
echo "🔧 Building backend image..."
docker build -t $BACKEND_IMAGE ./backend
if [ $? -ne 0 ]; then
    echo "❌ Failed to build backend image"
    exit 1
fi
echo "✅ Backend image built: $BACKEND_IMAGE"

# Build frontend image  
echo "🌐 Building frontend image..."
docker build -t $FRONTEND_IMAGE ./frontend
if [ $? -ne 0 ]; then
    echo "❌ Failed to build frontend image"
    exit 1
fi
echo "✅ Frontend image built: $FRONTEND_IMAGE"

# Show built images
echo ""
echo "📦 Built Images:"
docker images | grep -E "(vroomm-frontend|vroomm-backend)"

echo ""
echo "🚀 Images built successfully!"
echo ""
echo "Usage:"
echo "  Local: ./commands/build-images.sh"
echo "  With version: ./commands/build-images.sh v1.0"
echo "  With registry: ./commands/build-images.sh v1.0 your-registry.com"
echo ""
echo "To push to registry (if specified):"
echo "  docker push $FRONTEND_IMAGE"
echo "  docker push $BACKEND_IMAGE"