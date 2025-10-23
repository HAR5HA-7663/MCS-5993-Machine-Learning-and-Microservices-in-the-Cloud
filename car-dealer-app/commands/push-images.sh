#!/bin/bash

# Push Docker Images Script
echo "📤 Pushing Docker Images to Registry..."

VERSION=${1:-latest}
REGISTRY=${2}

if [ -z "$REGISTRY" ]; then
    echo "❌ Registry URL required"
    echo "Usage: ./commands/push-images.sh [version] [registry]"
    echo "Example: ./commands/push-images.sh v1.0 docker.io/yourusername"
    exit 1
fi

FRONTEND_IMAGE="$REGISTRY/vroomm-frontend:$VERSION"
BACKEND_IMAGE="$REGISTRY/vroomm-backend:$VERSION"

echo "Pushing images with version: $VERSION to $REGISTRY"

# Tag local images for registry
docker tag vroomm-frontend:$VERSION $FRONTEND_IMAGE
docker tag vroomm-backend:$VERSION $BACKEND_IMAGE

# Push images
echo "📤 Pushing frontend image..."
docker push $FRONTEND_IMAGE
if [ $? -ne 0 ]; then
    echo "❌ Failed to push frontend image"
    exit 1
fi

echo "📤 Pushing backend image..."
docker push $BACKEND_IMAGE  
if [ $? -ne 0 ]; then
    echo "❌ Failed to push backend image"
    exit 1
fi

echo "✅ All images pushed successfully!"
echo ""
echo "Images available at:"
echo "  $FRONTEND_IMAGE"
echo "  $BACKEND_IMAGE"