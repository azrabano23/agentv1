#!/bin/bash

echo "🔥 LAUNCHING AZRA BANO AI AGENT 🔥"
echo "=================================="
echo ""
echo "🚀 Starting the most badass AI agent..."
echo "⚡ Powered by cutting-edge technology"
echo "🛡️  Privacy-protected with O3 reasoning"
echo ""

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import flask, openai, chromadb" &> /dev/null; then
    echo "⚠️  Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✅ Dependencies ready"
echo "🌐 Starting web server..."
echo ""
echo "🎯 Your AI agent will be available at:"
echo "   http://localhost:5000"
echo ""
echo "🔥 Press Ctrl+C to stop the server"
echo ""

# Start the application
python3 app.py


