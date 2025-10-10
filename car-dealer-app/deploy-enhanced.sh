#!/bin/bash

# Enhanced Vroomm Vrommmm Car Dealership - Build and Deploy Script
# Run this script after starting Docker Desktop

set -e  # Exit on any error

echo "🚀 Building and Deploying Enhanced Car Dealership App to AWS ECS"
echo "================================================================"

# Variables
ECR_REGISTRY="898919247265.dkr.ecr.us-east-2.amazonaws.com"
ECR_REPO="vromm-vromm-car-management"
REGION="us-east-2"
CLUSTER_NAME="vroomm-cluster-99"

# Step 1: Login to ECR
echo "📝 Step 1: Authenticating with AWS ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Step 2: Build Backend Image
echo "🔨 Step 2: Building Enhanced Backend Image..."
docker build -t $ECR_REPO-backend:latest ./backend
docker build -t $ECR_REPO-backend:enhanced ./backend

# Step 3: Build Frontend Image  
echo "🎨 Step 3: Building Enhanced Frontend Image..."
docker build -t $ECR_REPO-frontend:latest ./frontend
docker build -t $ECR_REPO-frontend:enhanced ./frontend

# Step 4: Tag Images for ECR
echo "🏷️  Step 4: Tagging Images for ECR..."
docker tag $ECR_REPO-backend:latest $ECR_REGISTRY/$ECR_REPO:backend-latest
docker tag $ECR_REPO-backend:enhanced $ECR_REGISTRY/$ECR_REPO:backend-enhanced
docker tag $ECR_REPO-frontend:latest $ECR_REGISTRY/$ECR_REPO:frontend-latest  
docker tag $ECR_REPO-frontend:enhanced $ECR_REGISTRY/$ECR_REPO:frontend-enhanced

# Step 5: Push Images to ECR
echo "⬆️  Step 5: Pushing Images to ECR..."
docker push $ECR_REGISTRY/$ECR_REPO:backend-latest
docker push $ECR_REGISTRY/$ECR_REPO:backend-enhanced
docker push $ECR_REGISTRY/$ECR_REPO:frontend-latest
docker push $ECR_REGISTRY/$ECR_REPO:frontend-enhanced

# Step 6: Update ECS Task Definitions
echo "📋 Step 6: Creating Enhanced Task Definitions..."

# Create enhanced backend task definition
cat > backend-task-def-enhanced.json << EOF
{
  "family": "vroomm-backend-enhanced",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::898919247265:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "$ECR_REGISTRY/$ECR_REPO:backend-enhanced",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://postgres:admin123@vroomm-postgres-db.cxqcoc0okckd.us-east-2.rds.amazonaws.com:5432/cardealer"
        },
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/vroomm-backend-enhanced",
          "awslogs-region": "us-east-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

# Create enhanced frontend task definition
cat > frontend-task-def-enhanced.json << EOF
{
  "family": "vroomm-frontend-enhanced",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::898919247265:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "frontend",
      "image": "$ECR_REGISTRY/$ECR_REPO:frontend-enhanced",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/vroomm-frontend-enhanced",
          "awslogs-region": "us-east-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

# Step 7: Create Log Groups
echo "📝 Step 7: Creating CloudWatch Log Groups..."
aws logs create-log-group --log-group-name "/ecs/vroomm-backend-enhanced" --region $REGION 2>/dev/null || echo "Backend log group already exists"
aws logs create-log-group --log-group-name "/ecs/vroomm-frontend-enhanced" --region $REGION 2>/dev/null || echo "Frontend log group already exists"

# Step 8: Register Task Definitions
echo "📋 Step 8: Registering Enhanced Task Definitions..."
aws ecs register-task-definition --cli-input-json file://backend-task-def-enhanced.json --region $REGION
aws ecs register-task-definition --cli-input-json file://frontend-task-def-enhanced.json --region $REGION

# Step 9: Update ECS Services
echo "🔄 Step 9: Updating ECS Services..."

# Update backend service
aws ecs update-service \
  --cluster $CLUSTER_NAME \
  --service vroomm-backend-service \
  --task-definition vroomm-backend-enhanced \
  --desired-count 1 \
  --region $REGION

# Update frontend service  
aws ecs update-service \
  --cluster $CLUSTER_NAME \
  --service vroomm-frontend-service \
  --task-definition vroomm-frontend-enhanced \
  --desired-count 1 \
  --region $REGION

# Step 10: Wait for deployment
echo "⏳ Step 10: Waiting for services to update..."
echo "This may take 2-5 minutes..."

aws ecs wait services-stable \
  --cluster $CLUSTER_NAME \
  --services vroomm-backend-service vroomm-frontend-service \
  --region $REGION

# Step 11: Get new service IPs
echo "🌐 Step 11: Getting Updated Service Information..."

# Get backend service IP
BACKEND_TASK_ARN=$(aws ecs list-tasks \
  --cluster $CLUSTER_NAME \
  --service-name vroomm-backend-service \
  --region $REGION \
  --query 'taskArns[0]' \
  --output text)

if [ "$BACKEND_TASK_ARN" != "None" ] && [ "$BACKEND_TASK_ARN" != "" ]; then
  BACKEND_IP=$(aws ecs describe-tasks \
    --cluster $CLUSTER_NAME \
    --tasks $BACKEND_TASK_ARN \
    --region $REGION \
    --query 'tasks[0].attachments[0].details[?name==`publicIPv4Address`].value' \
    --output text)
  echo "✅ Enhanced Backend API: http://$BACKEND_IP:5000"
  echo "   📊 Statistics: http://$BACKEND_IP:5000/stats"
  echo "   🔍 Search: http://$BACKEND_IP:5000/search?q=Tesla"
  echo "   💚 Health: http://$BACKEND_IP:5000/health"
else
  echo "❌ Backend service not found or not running"
fi

# Get frontend service IP
FRONTEND_TASK_ARN=$(aws ecs list-tasks \
  --cluster $CLUSTER_NAME \
  --service-name vroomm-frontend-service \
  --region $REGION \
  --query 'taskArns[0]' \
  --output text)

if [ "$FRONTEND_TASK_ARN" != "None" ] && [ "$FRONTEND_TASK_ARN" != "" ]; then
  FRONTEND_IP=$(aws ecs describe-tasks \
    --cluster $CLUSTER_NAME \
    --tasks $FRONTEND_TASK_ARN \
    --region $REGION \
    --query 'tasks[0].attachments[0].details[?name==`publicIPv4Address`].value' \
    --output text)
  echo "✅ Enhanced Frontend UI: http://$FRONTEND_IP"
else
  echo "❌ Frontend service not found or not running"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "========================================"
echo ""
echo "🆕 NEW FEATURES AVAILABLE:"
echo "  📊 Statistics Dashboard - Real-time dealership analytics"
echo "  🔍 Advanced Search - Search cars by brand, model, VIN, year" 
echo "  👆 Interactive Cars - Click any car for detailed view"
echo "  ➕ Add New Cars - Enhanced form with validation"
echo "  🗑️  Bulk Delete - Select multiple cars to delete"
echo "  🎨 Modern UI - Professional design with animations"
echo ""
echo "🔗 API ENDPOINTS:"
echo "  GET /cars - List cars with sorting & pagination"
echo "  GET /cars/{vin} - Get individual car details"
echo "  POST /cars - Add new car"
echo "  PUT /cars/{vin} - Update car"
echo "  DELETE /cars - Delete multiple cars"
echo "  GET /search?q={query} - Search cars"
echo "  GET /stats - Dealership statistics"
echo "  GET /health - Health check"
echo ""
echo "📚 Documentation: See API_DOCUMENTATION.md for complete API reference"

# Cleanup temporary files
rm -f backend-task-def-enhanced.json frontend-task-def-enhanced.json

echo "🧹 Cleanup complete!"