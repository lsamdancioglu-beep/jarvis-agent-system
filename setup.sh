#!/bin/bash
# JARVIS Agent System Setup Script

echo "🤖 JARVIS Agent System Setup"
echo "============================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  Option 1 - CLI Mode:"
echo "    python3 main.py"
echo ""
echo "  Option 2 - Web Dashboard:"
echo "    python3 dashboard.py"
echo "    Then open: http://localhost:5000"
echo ""
echo "Try these commands in CLI mode:"
echo "  JARVIS> agents"
echo "  JARVIS> sessions"
echo "  JARVIS> analyze the repository"
echo "  JARVIS> dashboard"
echo ""
