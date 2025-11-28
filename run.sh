#!/bin/bash

# CP494 Job Application System - Startup Script

echo "🚀 Starting CP494 Job Application System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start n8n with Docker Compose
echo "📦 Starting n8n service..."
docker compose up -d

# Wait for n8n to be ready
echo "⏳ Waiting for n8n to start..."
sleep 10

# Check if n8n is accessible
if curl -s http://localhost:5678 > /dev/null; then
    echo "✅ n8n is running at http://localhost:5678"
    echo "   Login: admin / password"
else
    echo "⚠️  n8n might still be starting up. Check http://localhost:5678 in a moment."
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
pip install -r requirements.txt

# Start the FastAPI service
echo "🚀 Starting job processing API..."
python3 simple_api_service.py &
sleep 3

# Start the Gradio UI
echo "🌐 Starting web interface..."
cd ui
python3 app.py &

echo "
🎉 System is starting up!

📊 n8n Dashboard: http://localhost:5678
🚀 Job Processing API: http://localhost:8000
🌐 Web Interface: http://localhost:7860

📋 Next Steps:
1. Open the web interface and test job search
2. Run ./setup_workflows.sh for n8n workflow setup
3. Your Groq API key is already configured!

To stop everything:
  docker compose down
  pkill -f 'python3 simple_api_service.py'
  pkill -f 'python3 app.py'
"