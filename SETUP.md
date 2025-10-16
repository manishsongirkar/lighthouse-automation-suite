# 🔧 INITIAL SETUP GUIDE
## Complete Installation Instructions for Lighthouse Automation Suite

This guide covers setting up the Lighthouse Automation Suite from scratch, including scenarios where you don't have a virtual environment or dependencies installed.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.7+** installed on your system
- **Google Chrome browser** installed
- **Internet connection** for downloading dependencies
- **Terminal/Command Prompt** access

### Check Python Installation
```bash
python3 --version
# Should show: Python 3.x.x
```

If Python is not installed:
- **macOS**: Install from [python.org](https://www.python.org/downloads/) or use Homebrew: `brew install python3`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-pip python3-venv` (Ubuntu/Debian)

---

## 🚀 AUTOMATED SETUP (Recommended)

### Option 1: One-Click Setup Script

1. **Navigate to project directory:**
```bash
cd /path/to/lighthouse-automation-suite
```

2. **Run setup script:**
```bash
./setup.sh
```

The script will automatically:
- ✅ Check Python installation
- ✅ Create virtual environment (.venv/)
- ✅ Install all dependencies
- ✅ Create sample urls.txt
- ✅ Verify Chrome installation
- ✅ Test the setup

---

## 🛠️ MANUAL SETUP (Step-by-Step)

### Step 1: Create Project Directory
```bash
# If you don't have the project files yet
mkdir lighthouse-automation-suite
cd lighthouse-automation-suite

# Download or copy all project files into this directory
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# On Windows:
# .venv\\Scripts\\activate
```

**Important:** You should see `(.venv)` at the beginning of your terminal prompt when activated.

### Step 3: Upgrade Pip
```bash
# Make sure pip is up to date
pip install --upgrade pip
```

### Step 4: Install Dependencies

**Core dependencies:**
```bash
pip install selenium webdriver-manager fake-useragent
```

**Additional dependencies for reports:**
```bash
pip install pandas
```

**Or install all at once:**
```bash
pip install selenium webdriver-manager fake-useragent pandas
```

**Or use requirements.txt:**
```bash
pip install -r requirements.txt
```

### Step 5: Create URL Configuration File
```bash
# Create urls.txt with your target websites
cat > urls.txt << EOL
https://www.google.com
https://www.github.com
https://www.stackoverflow.com
EOL
```

### Step 6: Verify Setup
```bash
# Test that all modules can be imported
python -c "import selenium, pandas; print('✅ Setup successful!')"
```

---

## 🔄 STARTING FROM SCRATCH SCENARIOS

### Scenario 1: No .venv Directory Exists

```bash
# 1. Navigate to project directory
cd lighthouse-automation-suite

# 2. Create new virtual environment
python3 -m venv .venv

# 3. Activate it
source .venv/bin/activate

# 4. Install dependencies
pip install selenium webdriver-manager fake-useragent pandas

# 5. Ready to run!
python main.py
```

### Scenario 2: .venv Exists But Corrupted

```bash
# 1. Remove corrupted environment
rm -rf .venv

# 2. Create fresh environment
python3 -m venv .venv

# 3. Activate and install
source .venv/bin/activate
pip install selenium webdriver-manager fake-useragent pandas
```

### Scenario 3: Dependencies Missing

```bash
# Activate existing environment
source .venv/bin/activate

# Install missing packages
pip install selenium webdriver-manager fake-useragent pandas

# Or use requirements.txt if available
pip install -r requirements.txt
```

### Scenario 4: Fresh macOS/Linux System

```bash
# 1. Install Python 3 (if not installed)
# macOS with Homebrew:
brew install python3

# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip python3-venv

# 2. Install Chrome
# macOS: Download from google.com/chrome
# Ubuntu: wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# 3. Create project and setup
mkdir lighthouse-automation-suite
cd lighthouse-automation-suite
python3 -m venv .venv
source .venv/bin/activate
pip install selenium webdriver-manager fake-useragent pandas openpyxl
```

---

## ✅ VERIFICATION STEPS

After setup, verify everything works:

### 1. Check Virtual Environment
```bash
# Should show path ending in .venv/bin/python
which python
```

### 2. Test Selenium
```bash
python -c "from selenium import webdriver; print('Selenium OK')"
```

### 3. Test WebDriver Manager
```bash
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('WebDriver Manager OK')"
```

### 4. Test Complete Setup
```bash
python -c "
import selenium
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
print('✅ All dependencies working!')
"
```

### 5. Run Quick Test
```bash
# Make sure urls.txt exists and has content
cat urls.txt

# Run the tool
python main.py
```

---

## 🐛 TROUBLESHOOTING COMMON ISSUES

### Issue: "python3: command not found"
**Solution:** Install Python 3 from python.org or your system package manager

### Issue: "No module named 'selenium'"
**Solution:**
```bash
source .venv/bin/activate  # Make sure venv is activated
pip install selenium
```

### Issue: "Permission denied: ./setup.sh"
**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: "ChromeDriver not found"
**Solution:** The tool auto-downloads ChromeDriver, but ensure Chrome browser is installed

### Issue: Virtual environment activation not working
**Solution:**
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Or use absolute path
source /full/path/to/project/.venv/bin/activate
```

---

## 📦 DEPENDENCY REFERENCE

Here's what each dependency does:

- **selenium**: Web browser automation
- **webdriver-manager**: Automatic ChromeDriver management
- **fake-useragent**: Random user agent generation (anti-bot)
- **pandas**: Data processing and CSV handling
- **openpyxl**: Excel file support (optional)

---

## 🎯 QUICK START COMMANDS

**For someone starting completely fresh:**

```bash
# 1. Create and enter project directory
mkdir lighthouse-automation-suite && cd lighthouse-automation-suite

# 2. Download project files (copy main.py, etc. into this directory)

# 3. Run automated setup
chmod +x setup.sh && ./setup.sh

# 4. Edit URLs to test
nano urls.txt

# 5. Run analysis
python run_analysis.py
```

**For existing project without .venv:**

```bash
cd lighthouse-automation-suite
python3 -m venv .venv
source .venv/bin/activate
pip install selenium webdriver-manager fake-useragent pandas
python main.py
```

---

## 💡 Pro Tips

1. **Always activate virtual environment** before running scripts
2. **Use the automated setup script** for quickest installation
3. **Keep virtual environment** - don't delete .venv/ folder
4. **Update Chrome regularly** for best compatibility
5. **Start with small URL lists** to test everything works

---

**Need help?** Run `./setup.sh` for automated setup or follow the manual steps above! 🚀
