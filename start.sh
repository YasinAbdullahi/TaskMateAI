etassiss#!/bin/bash

# AI-Powered Todo List - Development Startup Script

echo "🤖 Starting AI-Powered Todo List Application..."
echo "================================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy env.example to .env and add your OpenAI API key:"
    echo "   cp env.example .env"
    echo "   # Then edit .env with your OPENAI_API_KEY"
    exit 1
fi

# Check if Python dependencies are installed
echo "🐍 Checking Python dependencies..."
if ! python -c "import flask, openai, flask_sqlalchemy" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if Node dependencies are installed
echo "📦 Checking Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo "🚀 Starting servers..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "================================================"

# Start backend server in background
echo "🔧 Starting Flask backend server..."
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "⚛️  Starting React frontend server..."
npm start &
FRONTEND_PID=$!

# Wait for user to stop
echo "✅ Both servers are running!"
echo "💡 Open http://localhost:3000 in your browser"
echo "🛑 Press Ctrl+C to stop both servers"

# Handle cleanup
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
