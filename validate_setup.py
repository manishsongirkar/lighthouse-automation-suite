#!/usr/bin/env python3
"""
Setup Validation Script for Lighthouse Automation Suite
Verifies that all components are properly installed and configured
"""
import sys
import os
import subprocess
from pathlib import Path

def print_colored(message, color="white"):
    """Print colored output"""
    colors = {
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{message}{colors['reset']}")

def check_python_version():
    """Check Python version"""
    print_colored("🐍 Checking Python version...", "cyan")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK", "green")
        return True
    else:
        print_colored(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.7+", "red")
        return False

def check_virtual_environment():
    """Check if virtual environment exists and is activated"""
    print_colored("📦 Checking virtual environment...", "cyan")

    # Check if .venv directory exists
    if not os.path.exists(".venv"):
        print_colored("❌ Virtual environment not found (.venv/)", "red")
        print_colored("   Run: python3 -m venv .venv", "yellow")
        return False

    # Check if currently in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_colored("✅ Virtual environment activated", "green")
        return True
    else:
        print_colored("⚠️  Virtual environment exists but not activated", "yellow")
        print_colored("   Run: source .venv/bin/activate", "yellow")
        return False

def check_required_files():
    """Check if all required project files exist"""
    print_colored("📁 Checking required project files...", "cyan")

    required_files = {
        "main.py": "Core analysis script",
        "run_analysis.py": "Complete workflow runner",
        "generate_html_report.py": "HTML dashboard generator",
        "requirements.txt": "Python dependencies",
        "urls.txt": "URLs to analyze"
    }

    all_good = True
    for file, description in required_files.items():
        if os.path.exists(file):
            print_colored(f"✅ {file} - {description}", "green")
        else:
            print_colored(f"❌ {file} - {description} (MISSING)", "red")
            all_good = False

    return all_good

def check_python_packages():
    """Check if all required Python packages are installed"""
    print_colored("📚 Checking Python packages...", "cyan")

    required_packages = {
        "selenium": "Web automation",
        "webdriver_manager": "ChromeDriver management",
        "fake_useragent": "Anti-detection",
        "pandas": "Data processing",
        "openpyxl": "Excel export"
    }

    all_good = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print_colored(f"✅ {package} - {description}", "green")
        except ImportError:
            print_colored(f"❌ {package} - {description} (NOT INSTALLED)", "red")
            all_good = False

    return all_good

def check_chrome_browser():
    """Check if Chrome browser is available"""
    print_colored("🌐 Checking Chrome browser...", "cyan")

    chrome_paths = {
        "darwin": ["/Applications/Google Chrome.app"],
        "linux": ["google-chrome", "chromium-browser"],
        "win32": [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    }

    platform = sys.platform
    if platform.startswith("darwin"):
        for path in chrome_paths["darwin"]:
            if os.path.exists(path):
                print_colored("✅ Google Chrome found (macOS)", "green")
                return True
    elif platform.startswith("linux"):
        for cmd in chrome_paths["linux"]:
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
                print_colored(f"✅ Chrome/Chromium found ({cmd})", "green")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    elif platform.startswith("win"):
        for path in chrome_paths["win32"]:
            if os.path.exists(path):
                print_colored("✅ Google Chrome found (Windows)", "green")
                return True

    print_colored("⚠️  Chrome browser not detected", "yellow")
    print_colored("   Chrome is required for Selenium automation", "yellow")
    return False

def check_chromedriver():
    """Test ChromeDriver download capability"""
    print_colored("🚗 Testing ChromeDriver download...", "cyan")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print_colored("✅ ChromeDriver download successful", "green")
        return True
    except Exception as e:
        print_colored(f"❌ ChromeDriver download failed: {e}", "red")
        return False

def validate_urls_file():
    """Validate URLs in urls.txt"""
    print_colored("🔗 Validating URLs file...", "cyan")

    if not os.path.exists("urls.txt"):
        print_colored("❌ urls.txt not found", "red")
        return False

    valid_urls = 0
    invalid_lines = 0
    total_lines = 0

    with open("urls.txt", "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            clean_line = line.strip()

            # Skip empty lines and comments
            if not clean_line or clean_line.startswith("#"):
                continue

            if clean_line.startswith(("http://", "https://")):
                valid_urls += 1
            else:
                invalid_lines += 1

    print_colored(f"📊 URLs file analysis:", "blue")
    print_colored(f"   Total lines: {total_lines}", "white")
    print_colored(f"   Valid URLs: {valid_urls}", "green" if valid_urls > 0 else "yellow")

    if invalid_lines > 0:
        print_colored(f"   Invalid lines: {invalid_lines}", "yellow")

    if valid_urls == 0:
        print_colored("⚠️  No valid URLs found for analysis", "yellow")
        print_colored("   Add URLs starting with http:// or https://", "yellow")
        return False

    print_colored("✅ URLs file validated", "green")
    return True

def test_basic_functionality():
    """Test basic script functionality"""
    print_colored("🧪 Testing basic functionality...", "cyan")

    try:
        # Test imports that would be used in main.py
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from fake_useragent import UserAgent
        import pandas as pd

        print_colored("✅ Core imports successful", "green")

        # Test UserAgent
        ua = UserAgent()
        user_agent = ua.random
        print_colored("✅ User agent generation working", "green")

        # Test pandas basic functionality
        test_data = {"test": [1, 2, 3]}
        df = pd.DataFrame(test_data)
        print_colored("✅ Pandas data processing working", "green")

        return True

    except Exception as e:
        print_colored(f"❌ Functionality test failed: {e}", "red")
        return False

def main():
    """Main validation function"""
    print_colored("🚀 Lighthouse Automation Suite - Setup Validation", "blue")
    print_colored("=" * 60, "blue")
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Required Files", check_required_files),
        ("Python Packages", check_python_packages),
        ("Chrome Browser", check_chrome_browser),
        ("ChromeDriver", check_chromedriver),
        ("URLs File", validate_urls_file),
        ("Basic Functionality", test_basic_functionality)
    ]

    results = []
    for check_name, check_func in checks:
        print()
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_colored(f"❌ {check_name} check failed with error: {e}", "red")
            results.append((check_name, False))

    # Summary
    print()
    print_colored("=" * 60, "blue")
    print_colored("📋 VALIDATION SUMMARY", "blue")
    print_colored("=" * 60, "blue")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = "green" if result else "red"
        print_colored(f"{status} - {check_name}", color)

    print()
    if passed == total:
        print_colored("🎉 ALL CHECKS PASSED!", "green")
        print_colored("Your setup is ready for PageSpeed analysis!", "green")
        print()
        print_colored("🚀 Next steps:", "blue")
        print_colored("1. Edit urls.txt with your target websites", "white")
        print_colored("2. Run: python run_analysis.py", "white")
    else:
        print_colored(f"⚠️  {total - passed} checks failed out of {total}", "yellow")
        print_colored("Please fix the failing checks before running analysis.", "yellow")
        print()
        print_colored("💡 To fix issues:", "blue")
        print_colored("• Re-run setup.sh for installation problems", "white")
        print_colored("• Activate virtual environment: source .venv/bin/activate", "white")
        print_colored("• Install missing packages: pip install -r requirements.txt", "white")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
