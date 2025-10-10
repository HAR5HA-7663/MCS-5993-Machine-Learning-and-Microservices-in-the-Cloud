#!/bin/bash

# Local Development Setup Script
echo "🔧 Setting up Vroomm Vrommmm for local development..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL first."
    echo "   Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "   macOS: brew install postgresql"
    echo "   Windows: Download from https://www.postgresql.org/"
    exit 1
fi

# Setup backend
echo "🐍 Setting up Python backend..."
cd backend/

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Set environment variable
export DATABASE_URL="postgres://caruser:carpass@localhost:5432/cardb"
echo "✅ Environment variables set"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create PostgreSQL database:"
echo "   sudo -u postgres psql -c \"CREATE DATABASE cardb;\""
echo "   sudo -u postgres psql -c \"CREATE USER caruser WITH PASSWORD 'carpass';\""
echo "   sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE cardb TO caruser;\""
echo ""
echo "2. Run the application:"
echo "   ./commands/run-local.sh"
echo ""
echo "3. Access the app:"
echo "   Frontend: http://localhost:8080"
echo "   Backend API: http://localhost:5000"