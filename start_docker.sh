#!/bin/bash
# Quick Start Script for MkDocs with Docker

set -e

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║     MkDocs with RAG & Docker - Quick Start                            ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and set SOURCE_CODE_PATH"
    echo ""
fi

# Start services
echo "🚀 Starting Docker services..."
echo ""
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check services
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║  Services Started Successfully!                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Documentation:    http://localhost:8000"
echo "🤖 Chatbot API:      http://localhost:8765"
echo "🗄️  Qdrant Dashboard: http://localhost:6333/dashboard"
echo "💾 MinIO Console:    http://localhost:9001"
echo "    Login: admin / password123"
echo ""
echo "📋 View logs:"
echo "    docker-compose logs -f mkdocs"
echo ""
echo "🛑 Stop services:"
echo "    docker-compose down"
echo ""
