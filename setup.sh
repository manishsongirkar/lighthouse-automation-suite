#!/bin/bash
# 🚀 Lighthouse Automation Suite - Enhanced Setup Script
# This script sets up everything you need to run the PageSpeed automation tool
# Supports macOS, Linux, and Windows (via Git Bash/WSL)

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_status $BLUE "🚀 Lighthouse Automation Suite - Enhanced Setup Script"
print_status $BLUE "============================================================"
echo ""

# Step 1: Check Operating System
print_status $CYAN "📋 Step 1: Detecting operating system..."
OS="unknown"
case "$OSTYPE" in
    darwin*)  OS="macOS" ;;
    linux*)   OS="Linux" ;;
    msys*|mingw*|cygwin*) OS="Windows" ;;
    *)        OS="Other" ;;
esac
print_status $GREEN "✅ Detected OS: $OS"

# Step 2: Check if Python 3 is installed
print_status $CYAN "📋 Step 2: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_status $RED "❌ Python 3 is not installed."
    echo ""
    print_status $YELLOW "📥 Please install Python 3.7+ first:"
    case $OS in
        "macOS")
            echo "   • Download from: https://www.python.org/downloads/"
            echo "   • Or use Homebrew: brew install python3"
            ;;
        "Linux")
            echo "   • Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
            echo "   • CentOS/RHEL: sudo yum install python3 python3-pip"
            echo "   • Fedora: sudo dnf install python3 python3-pip"
            ;;
        "Windows")
            echo "   • Download from: https://www.python.org/downloads/"
            echo "   • Or use Chocolatey: choco install python3"
            ;;
    esac
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
print_status $GREEN "✅ Python found: $PYTHON_VERSION"

# Check Python version (should be 3.7+)
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    print_status $RED "❌ Python 3.7+ is required. Found: $PYTHON_VERSION"
    print_status $YELLOW "Please upgrade to Python 3.7 or newer."
    exit 1
fi

# Step 3: Check if we're in the right directory
print_status $CYAN "📋 Step 3: Validating project directory..."
REQUIRED_FILES=("main.py" "run_analysis.py" "generate_html_report.py" "requirements.txt")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    print_status $RED "❌ Missing required files: ${MISSING_FILES[*]}"
    print_status $YELLOW "Please run this script from the lighthouse-automation-suite project directory."
    echo ""
    print_status $CYAN "Expected project structure:"
    for file in "${REQUIRED_FILES[@]}"; do
        echo "   📄 $file"
    done
    exit 1
fi

print_status $GREEN "✅ Project directory validated"

# Step 4: Create virtual environment
print_status $CYAN "📋 Step 4: Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    print_status $YELLOW "📦 Creating Python virtual environment..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        print_status $GREEN "✅ Virtual environment created successfully"
    else
        print_status $RED "❌ Failed to create virtual environment"
        print_status $YELLOW "💡 Try: python3 -m pip install --upgrade pip setuptools"
        exit 1
    fi
else
    print_status $GREEN "✅ Virtual environment already exists"
fi

# Step 5: Activate virtual environment
print_status $CYAN "� Step 5: Activating virtual environment..."
case $OS in
    "Windows")
        if [ -f ".venv/Scripts/activate" ]; then
            source .venv/Scripts/activate
        else
            print_status $RED "❌ Windows virtual environment activation failed"
            exit 1
        fi
        ;;
    *)
        if [ -f ".venv/bin/activate" ]; then
            source .venv/bin/activate
        else
            print_status $RED "❌ Virtual environment activation failed"
            exit 1
        fi
        ;;
esac
print_status $GREEN "✅ Virtual environment activated"

# Step 6: Upgrade pip and install build tools
print_status $CYAN "� Step 6: Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel
if [ $? -eq 0 ]; then
    print_status $GREEN "✅ Pip and build tools upgraded"
else
    print_status $YELLOW "⚠️  Warning: Failed to upgrade pip/build tools, continuing..."
fi

# Step 7: Install Python dependencies from requirements.txt
print_status $CYAN "� Step 7: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    print_status $YELLOW "📦 Installing from requirements.txt..."
    python -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_status $GREEN "✅ All Python dependencies installed successfully"
    else
        print_status $RED "❌ Failed to install dependencies from requirements.txt"
        print_status $YELLOW "🔄 Attempting manual installation of core packages..."

        # Fallback: Install core packages manually
        CORE_PACKAGES=("selenium>=4.0.0" "webdriver-manager>=4.0.0" "fake-useragent>=1.4.0" "pandas>=2.0.0" "openpyxl>=3.1.0")
        for package in "${CORE_PACKAGES[@]}"; do
            print_status $YELLOW "Installing $package..."
            python -m pip install "$package"
        done
    fi
else
    print_status $RED "❌ requirements.txt not found!"
    exit 1
fi

# Step 8: Create or validate urls.txt
print_status $CYAN "📋 Step 8: Setting up URLs file..."
if [ ! -f "urls.txt" ]; then
    print_status $YELLOW "📝 Creating sample urls.txt file..."
    cat > urls.txt << 'EOL'
# Lighthouse Automation Suite - URLs to analyze
# Add one URL per line (must start with http:// or https://)
# Lines starting with # are comments and will be ignored

# Example URLs (replace with your own):
https://www.google.com
https://www.github.com

# Add your URLs below:
# https://www.yourwebsite.com
# https://www.competitor.com
EOL
    print_status $GREEN "✅ Sample urls.txt created with examples"
else
    print_status $GREEN "✅ urls.txt already exists"

    # Validate existing URLs
    VALID_URLS=0
    INVALID_LINES=0
    while IFS= read -r line; do
        # Skip empty lines and comments
        if [[ -z "$line" ]] || [[ "$line" =~ ^[[:space:]]*# ]]; then
            continue
        fi

        if [[ "$line" =~ ^https?:// ]]; then
            ((VALID_URLS++))
        else
            ((INVALID_LINES++))
        fi
    done < urls.txt

    if [ $VALID_URLS -gt 0 ]; then
        print_status $GREEN "   📊 Found $VALID_URLS valid URLs ready for analysis"
        if [ $INVALID_LINES -gt 0 ]; then
            print_status $YELLOW "   ⚠️  Found $INVALID_LINES invalid lines (will be skipped)"
        fi
    else
        print_status $YELLOW "   ⚠️  No valid URLs found. Please add URLs to analyze."
    fi
fi

# Step 9: Check for Chrome browser
print_status $CYAN "📋 Step 9: Checking for Chrome browser..."
CHROME_FOUND=false

case $OS in
    "macOS")
        if [ -d "/Applications/Google Chrome.app" ]; then
            CHROME_FOUND=true
            CHROME_VERSION=$(defaults read "/Applications/Google Chrome.app/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null || echo "unknown")
            print_status $GREEN "✅ Google Chrome found (version: $CHROME_VERSION)"
        fi
        ;;
    "Linux")
        if command -v google-chrome &> /dev/null; then
            CHROME_FOUND=true
            CHROME_VERSION=$(google-chrome --version 2>/dev/null | cut -d' ' -f3 || echo "unknown")
            print_status $GREEN "✅ Google Chrome found (version: $CHROME_VERSION)"
        elif command -v chromium-browser &> /dev/null; then
            CHROME_FOUND=true
            CHROME_VERSION=$(chromium-browser --version 2>/dev/null | cut -d' ' -f2 || echo "unknown")
            print_status $GREEN "✅ Chromium browser found (version: $CHROME_VERSION)"
        fi
        ;;
    "Windows")
        # Check common Chrome installation paths on Windows
        CHROME_PATHS=(
            "/c/Program Files/Google/Chrome/Application/chrome.exe"
            "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
            "$LOCALAPPDATA/Google/Chrome/Application/chrome.exe"
        )

        for path in "${CHROME_PATHS[@]}"; do
            if [ -f "$path" ]; then
                CHROME_FOUND=true
                print_status $GREEN "✅ Google Chrome found at: $path"
                break
            fi
        done
        ;;
esac

if [ "$CHROME_FOUND" = false ]; then
    print_status $YELLOW "⚠️  Google Chrome not found."
    echo ""
    print_status $CYAN "📥 Chrome installation instructions:"
    case $OS in
        "macOS")
            echo "   • Download from: https://www.google.com/chrome/"
            echo "   • Or use Homebrew: brew install --cask google-chrome"
            ;;
        "Linux")
            echo "   • Ubuntu/Debian: wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && sudo apt install google-chrome-stable"
            echo "   • Or download from: https://www.google.com/chrome/"
            ;;
        "Windows")
            echo "   • Download from: https://www.google.com/chrome/"
            echo "   • Or use Chocolatey: choco install googlechrome"
            ;;
    esac
    print_status $YELLOW "Note: Chrome is required for Selenium automation to work properly."
fi

# Step 10: Test installation comprehensively
print_status $CYAN "📋 Step 10: Testing installation..."

print_status $YELLOW "🧪 Testing Python module imports..."
python -c "
try:
    import selenium
    print('✅ Selenium: OK')
except ImportError as e:
    print(f'❌ Selenium: FAILED - {e}')
    exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print('✅ WebDriver Manager: OK')
except ImportError as e:
    print(f'❌ WebDriver Manager: FAILED - {e}')
    exit(1)

try:
    from fake_useragent import UserAgent
    print('✅ Fake User Agent: OK')
except ImportError as e:
    print(f'❌ Fake User Agent: FAILED - {e}')
    exit(1)

try:
    import pandas
    print('✅ Pandas: OK')
except ImportError as e:
    print(f'❌ Pandas: FAILED - {e}')
    exit(1)

try:
    import openpyxl
    print('✅ OpenPyXL: OK')
except ImportError as e:
    print(f'❌ OpenPyXL: FAILED - {e}')
    exit(1)

print('✅ All core modules imported successfully')
"

if [ $? -ne 0 ]; then
    print_status $RED "❌ Module import test failed"
    print_status $YELLOW "🔄 Try reinstalling dependencies:"
    echo "   pip install --force-reinstall -r requirements.txt"
    exit 1
fi

# Test WebDriver download capability
print_status $YELLOW "🧪 Testing ChromeDriver auto-download..."
python -c "
try:
    from webdriver_manager.chrome import ChromeDriverManager
    driver_path = ChromeDriverManager().install()
    print(f'✅ ChromeDriver downloaded successfully: {driver_path}')
except Exception as e:
    print(f'❌ ChromeDriver download failed: {e}')
    exit(1)
" 2>/dev/null

if [ $? -ne 0 ]; then
    print_status $YELLOW "⚠️  ChromeDriver test had issues, but installation should still work"
fi

print_status $GREEN "✅ Installation testing completed"

# Step 11: Final setup summary and next steps
echo ""
print_status $GREEN "🎉 SETUP COMPLETED SUCCESSFULLY!"
print_status $GREEN "============================================================"
echo ""

print_status $BLUE "📋 What was installed and configured:"
print_status $GREEN "   ✅ Python virtual environment (.venv/)"
print_status $GREEN "   ✅ Selenium WebDriver (latest version)"
print_status $GREEN "   ✅ WebDriver Manager (auto-downloads ChromeDriver)"
print_status $GREEN "   ✅ Fake User Agent (anti-detection)"
print_status $GREEN "   ✅ Pandas (data processing and CSV export)"
print_status $GREEN "   ✅ OpenPyXL (Excel export capability)"
print_status $GREEN "   ✅ Sample URLs file (urls.txt) with examples"
if [ "$CHROME_FOUND" = true ]; then
    print_status $GREEN "   ✅ Google Chrome browser detected"
else
    print_status $YELLOW "   ⚠️  Chrome browser needs to be installed separately"
fi

echo ""
print_status $BLUE "🚀 Ready to start analyzing!"
print_status $CYAN "============================================================"
echo ""

print_status $PURPLE "📝 Next Steps:"
print_status $YELLOW "1. Edit urls.txt with your target websites:"
echo "   nano urls.txt    # or use any text editor"
echo ""
print_status $YELLOW "2. Run the complete analysis workflow:"
echo "   python run_analysis.py"
echo ""
print_status $YELLOW "3. Or run individual components:"
echo "   python main.py                    # Core analysis only"
echo "   python generate_html_report.py    # Generate dashboard only"
echo ""

print_status $PURPLE "💡 Pro Tips:"
print_status $CYAN "• Use 'python run_analysis.py' for the complete workflow (recommended)"
print_status $CYAN "• Enable screenshots for detailed visual documentation"
print_status $CYAN "• Start with a small batch of URLs (5-10) to test the setup"
print_status $CYAN "• The HTML dashboard will auto-open in your browser when complete"
echo ""

print_status $PURPLE "🔧 For future sessions, remember to activate the virtual environment:"
case $OS in
    "Windows")
        echo "   .venv\\Scripts\\activate"
        ;;
    *)
        echo "   source .venv/bin/activate"
        ;;
esac
echo ""

print_status $PURPLE "📊 Expected output files:"
print_status $CYAN "• pagespeed_results.csv - Core performance metrics"
print_status $CYAN "• pagespeed_report.html - Interactive performance dashboard"
print_status $CYAN "• screenshots-YYYYMMDD_HHMMSS/ - Full HD screenshots (if enabled)"
echo ""

# Check if there are URLs ready to analyze
VALID_URLS=$(grep -c '^https\?://' urls.txt 2>/dev/null || echo 0)
if [ $VALID_URLS -gt 0 ]; then
    print_status $GREEN "🎯 You have $VALID_URLS URLs ready for analysis!"
    echo ""
    print_status $YELLOW "Want to start analyzing now? Run:"
    echo "   python run_analysis.py"
else
    print_status $YELLOW "📝 Please add your URLs to urls.txt before running the analysis."
fi

echo ""
print_status $GREEN "Happy analyzing! 🎉"
