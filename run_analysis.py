#!/usr/bin/env python3
"""
Lighthouse Automation Suite Runner
Complete workflow script for Lighthouse analysis and reporting
"""
import subprocess
import sys
import os
import webbrowser
from pathlib import Path

def cleanup_existing_files():
    """Clean up existing result files before starting new analysis"""
    files_to_cleanup = [
        "pagespeed_results.csv",
        "pagespeed_report.html"
    ]
    cleaned_files = []

    print("🧹 Cleaning up existing result files...")

    for filename in files_to_cleanup:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                cleaned_files.append(filename)
                print(f"   🗑️  Removed: {filename}")
            except Exception as e:
                print(f"   ❌ Failed to remove {filename}: {e}")
                return False
        else:
            print(f"   ℹ️  {filename} does not exist (skip)")

    if cleaned_files:
        print(f"✅ Cleanup completed - removed {len(cleaned_files)} file(s)")
    else:
        print("✅ Cleanup completed - no files to remove")

    return True

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        # Run command without capturing output to show real-time progress
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with exit code: {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def main():
    """Main execution workflow"""
    print("🚀 Lighthouse Automation Suite Workflow")
    print("=" * 50)

    # Clean up existing result files first
    if not cleanup_existing_files():
        print("❌ Cleanup failed. Exiting.")
        return False

    # Get Python path dynamically (cross-platform)
    current_dir = os.getcwd()

    # Determine virtual environment Python path based on OS
    if os.name == 'nt':  # Windows
        venv_python = os.path.join(current_dir, ".venv", "Scripts", "python.exe")
        fallback_python = "python"
        activate_cmd = ".venv\\Scripts\\activate"
    else:  # macOS/Linux
        venv_python = os.path.join(current_dir, ".venv", "bin", "python")
        fallback_python = "python3"
        activate_cmd = "source .venv/bin/activate"

    # Check if virtual environment exists
    if os.path.exists(venv_python):
        python_path = venv_python
        print(f"✅ Using virtual environment: {os.path.relpath(python_path)}")
    else:
        # Fallback to system python
        python_path = fallback_python
        print("⚠️  Virtual environment not found, using system Python")
        print(f"💡 To create venv: python3 -m venv .venv && {activate_cmd}")

    # Check if URLs file exists
    if not os.path.exists("urls.txt"):
        print("❌ urls.txt not found!")
        print("📝 Please create urls.txt with your target URLs (one per line)")
        return False

    # Validate and count URLs using same logic as main.py
    valid_urls = []
    invalid_lines = []
    total_lines = 0

    with open("urls.txt", "r", encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            # Strip whitespace
            clean_line = line.strip()

            # Skip empty lines
            if not clean_line:
                continue

            # Skip comment lines (starting with #)
            if clean_line.startswith('#'):
                continue

            # Basic URL validation - must start with http:// or https://
            if clean_line.startswith(('http://', 'https://')):
                valid_urls.append(clean_line)
            else:
                invalid_lines.append(f"Line {line_num}: '{clean_line}'")

    # Show detailed URL analysis
    print(f"📊 URL Analysis Results:")
    print(f"   📄 Total lines in file: {total_lines}")
    print(f"   ✅ Valid URLs found: {len(valid_urls)}")

    if invalid_lines:
        print(f"   ⚠️  Invalid lines skipped: {len(invalid_lines)}")
        if len(invalid_lines) <= 3:
            for invalid in invalid_lines:
                print(f"      • {invalid}")
        else:
            for invalid in invalid_lines[:2]:
                print(f"      • {invalid}")
            print(f"      • ... and {len(invalid_lines)-2} more")

    if not valid_urls:
        print("❌ No valid URLs found to analyze!")
        print("💡 URLs must start with 'http://' or 'https://'")
        return False

    # Ask user if they want Full HD screenshot capture
    response = input("\n📸 Enable Full HD full-page screenshot capture? (Y/n): ").lower().strip()
    enable_screenshots = response != 'n'

    # Step 1: Run optimized Lighthouse analysis (with integrated Full HD screenshot support)
    analysis_command = f"{python_path} main.py"
    if enable_screenshots:
        # Pass 'Y' input to enable screenshots
        analysis_command = f"echo 'Y' | {python_path} main.py"
        print("📸 Using optimized script with Full HD screenshot capture")
    else:
        # Pass 'n' input to disable screenshots
        analysis_command = f"echo 'n' | {python_path} main.py"
        print("📊 Using optimized script without screenshots")

    if not run_command(analysis_command, "Optimized Lighthouse Analysis with Full HD Screenshots" if enable_screenshots else "Optimized Lighthouse Analysis"):
        return False

    # Step 2: Generate HTML dashboard
    if not run_command(f"{python_path} generate_html_report.py", "HTML Dashboard Generation"):
        return False

    # Summary
    print("\n" + "=" * 50)
    print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\n📂 Generated Files:")
    print("   📊 pagespeed_results.csv     - Core performance metrics and scores")
    print("   🎯 pagespeed_report.html     - Performance dashboard")

    # Check for screenshot directory if screenshots were enabled
    if enable_screenshots:
        screenshot_dirs = [d for d in os.listdir('.') if d.startswith('screenshots-') and os.path.isdir(d)]
        if screenshot_dirs:
            # Get the most recent screenshot directory
            screenshot_dir = sorted(screenshot_dirs)[-1]
            screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
            if screenshots:
                print(f"   📸 {screenshot_dir}/     - Full HD Screenshots ({len(screenshots)} files)")
                fullhd_mobile_screenshots = [f for f in screenshots if f.startswith('fullhd_mobile_')]
                fullhd_desktop_screenshots = [f for f in screenshots if f.startswith('fullhd_desktop_')]
                print(f"       � Mobile: {len(fullhd_mobile_screenshots)} | 🖥️  Desktop: {len(fullhd_desktop_screenshots)}")

    # Offer to open HTML report
    response = input("\n🌐 Open HTML report in browser? (y/n): ").lower().strip()
    if response == 'y':
        html_path = os.path.abspath("pagespeed_report.html")
        webbrowser.open(f"file://{html_path}")
        print("✅ HTML report opened in browser")

    # Offer to open screenshot directory if screenshots were enabled
    if enable_screenshots and screenshot_dirs:
        response = input("\n📂 Open Full HD screenshot directory? (y/n): ").lower().strip()
        if response == 'y':
            screenshot_path = os.path.abspath(screenshot_dir)
            if os.name == 'nt':  # Windows
                os.startfile(screenshot_path)
            elif os.name == 'posix':  # macOS/Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', screenshot_path])
                else:  # Linux
                    subprocess.run(['xdg-open', screenshot_path])
            print(f"✅ Screenshot directory opened: {screenshot_dir}")

    print("\n�💡 Next Steps:")
    print("   • Review the performance dashboard for visual insights")
    print("   • Import CSV data into Excel/Google Sheets for further analysis")
    if enable_screenshots:
        print("   • Check Full HD screenshot files for complete page verification")
    print("   • Focus on URLs with Core Web Vitals issues")
    print("   • Re-run analysis after implementing optimizations")

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
