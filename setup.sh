#!/bin/bash
# 🚀 Lighthouse Automation Suite - Initial Setup Script
# This script sets up everything you need to run the PageSpeed automation tool

echo "🚀 Lighthouse Automation Suite - Setup Script"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the project directory."
    exit 1
fi

echo "✅ Project directory confirmed"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created successfully"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install selenium webdriver-manager fake-useragent pandas openpyxl

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create urls.txt if it doesn't exist
if [ ! -f "urls.txt" ]; then
    echo "📝 Creating sample urls.txt file..."
    cat > urls.txt << EOL
https://www.google.com
https://www.github.com
EOL
    echo "✅ Sample urls.txt created"
else
    echo "✅ urls.txt already exists"
fi

# Check if Chrome is installed (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "✅ Google Chrome found"
    else
        echo "⚠️  Google Chrome not found. Please install Chrome for the tool to work."
        echo "   Download from: https://www.google.com/chrome/"
    fi
fi

# Test installation
echo "🧪 Testing installation..."
python -c "import selenium; import pandas; print('✅ All modules imported successfully')"

echo ""
echo "🎉 SETUP COMPLETE!"
echo "=================="
echo ""
echo "📋 What was installed:"
echo "   ✅ Python virtual environment (.venv/)"
echo "   ✅ Selenium WebDriver"
echo "   ✅ WebDriver Manager (auto-downloads ChromeDriver)"
echo "   ✅ Fake User Agent"
echo "   ✅ Pandas (for data processing)"
echo "   ✅ OpenPyXL (for Excel export)"
echo "   ✅ Sample URLs file (urls.txt)"
echo ""
echo "🚀 Ready to run!"
echo "   Edit urls.txt with your target websites"
echo "   Then run: python run_analysis.py"
echo ""
echo "💡 Remember to activate the virtual environment in future sessions:"
echo "   source .venv/bin/activate"
