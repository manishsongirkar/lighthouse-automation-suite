import csv
import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Global screenshot directory to persist across all URLs in a session
SCREENSHOT_DIR = None
def initialize_screenshot_directory():
    """Initialize a single screenshot directory for the entire session"""
    global SCREENSHOT_DIR
    if SCREENSHOT_DIR is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        SCREENSHOT_DIR = f"screenshots-{timestamp}"

        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
            print(f"📁 Created screenshot directory: {SCREENSHOT_DIR}")

    return SCREENSHOT_DIR

def capture_full_hd_screenshots(driver, url, url_index, enable_screenshots=False):
    """
    Capture optimized Full HD full-page screenshots for both mobile and desktop views
    Args:
        driver: Selenium WebDriver instance
        url: URL being tested
        url_index: Index of the current URL
        enable_screenshots: Whether to capture screenshots
    """
    if not enable_screenshots:
        return

    try:
        screenshot_dir = initialize_screenshot_directory()
        print("📸 Capturing Full HD screenshots for mobile and desktop...")

        # Create safe filename from URL
        safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        if len(safe_url) > 50:
            safe_url = safe_url[:50]

        # Capture mobile view screenshot
        capture_device_full_hd_screenshot(driver, "mobile", screenshot_dir, url_index, safe_url)

        # Capture desktop view screenshot
        capture_device_full_hd_screenshot(driver, "desktop", screenshot_dir, url_index, safe_url)

    except Exception as e:
        print(f"⚠️  Full HD screenshot capture failed for {url}: {e}")

def capture_device_full_hd_screenshot(driver, device_type, screenshot_dir, url_index, safe_url):
    """Capture Full HD screenshot for specific device view"""
    try:
        # Try to find and click the device tab
        device_selectors = {
            "mobile": ["[data-testid='device-mobile']", "button[aria-label*='Mobile']", "button[aria-label*='mobile']"],
            "desktop": ["[data-testid='device-desktop']", "button[aria-label*='Desktop']", "button[aria-label*='desktop']"]
        }

        tab_found = False
        for selector in device_selectors[device_type]:
            try:
                tab = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                tab.click()
                tab_found = True
                break
            except:
                continue

        if not tab_found:
            # Use JavaScript fallback to find device tabs
            tab = driver.execute_script(f"""
                const buttons = document.querySelectorAll('button, [role="tab"]');
                for (let btn of buttons) {{
                    const text = btn.textContent.toLowerCase();
                    const label = btn.getAttribute('aria-label')?.toLowerCase() || '';
                    if (text.includes('{device_type}') || label.includes('{device_type}')) {{
                        return btn;
                    }}
                }}
                return null;
            """)
            if tab:
                driver.execute_script("arguments[0].click();", tab)
                tab_found = True

        if tab_found:
            print(f"{'📱' if device_type == 'mobile' else '🖥️'} Switched to {device_type} view")
            time.sleep(2)  # Wait for tab content to load
        else:
            print(f"⚠️  Could not find {device_type} tab, capturing current view")

        # Get the total page height for full-page capture
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

        # Set Full HD window size and capture full page
        driver.set_window_size(1920, max(1080, total_height))

        # Brief wait for content to render at new size
        time.sleep(1)

        # Capture Full HD screenshot
        filename = f"{screenshot_dir}/fullhd_{device_type}_{url_index:02d}_{safe_url}.png"
        driver.save_screenshot(filename)
        print(f"✅ Full HD {device_type} screenshot saved: {filename}")
        return True

    except Exception as e:
        print(f"⚠️  Could not capture Full HD {device_type} screenshot: {e}")
        return False

def get_pagespeed_results(url_to_test, current_index=1, total_urls=1, enable_screenshots=False):
    """
    Gets Lighthouse scores by directly navigating to PageSpeed Insights analysis URL.
    Extracts both mobile and desktop scores from JSON objects and optionally captures screenshots.
    Args:
        url_to_test (str): The URL to be tested by Lighthouse via PageSpeed Insights.
        current_index (int): Current URL index being processed.
        total_urls (int): Total number of URLs to process.
        enable_screenshots (bool): Whether to capture screenshots.
    Returns:
        dict: A dictionary containing mobile scores, desktop scores, and final URL, or None if an error occurs.
    """
    progress_percent = (current_index / total_urls) * 100
    print("=" * 60)
    print(f"🔄 Processing URL {current_index}/{total_urls} ({progress_percent:.1f}%)")
    print(f"📊 Current URL: {url_to_test}")
    print("=" * 60)

    # --- Setup Selenium WebDriver with optimized performance ---
    options = webdriver.ChromeOptions()

    # Use a random user agent to mimic a real browser
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")

    # Performance-optimized browser settings
    options.add_argument("--headless")  # Run in headless mode for better performance
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-extensions")  # Disable all extensions
    options.add_argument("--disable-plugins")  # Disable plugins
    options.add_argument("--disable-default-apps")  # Disable default apps
    options.add_argument("--aggressive-cache-discard")  # More aggressive memory management
    options.add_argument("--memory-pressure-off")  # Turn off memory pressure checks

    # Anti-bot detection measures (minimal set for performance)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    print("🔧 Chrome optimized: Headless mode, performance-focused settings")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Use JavaScript to modify navigator.webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    try:
        # Navigate directly to the analysis URL
        analysis_url = f"https://pagespeed.web.dev/analysis?url={url_to_test}"
        print(f"Navigating to: {analysis_url}")
        driver.get(analysis_url)

        print("⏳ Waiting for analysis to complete...")        # Optimized wait for Lighthouse JSON data (reduced from 180s to 120s)
        print("⚡ Waiting for Lighthouse JSON data (optimized timeout: 120s)...")

        # Wait for at least one of the JSON objects to be available
        WebDriverWait(driver, 120).until(
            lambda driver: driver.execute_script(
                "return window.__LIGHTHOUSE_MOBILE_JSON__ || window.__LIGHTHOUSE_DESKTOP_JSON__;"
            )
        )

        print("✅ Initial Lighthouse JSON data detected.")

        # Reduced additional wait time for both datasets
        print("⚡ Waiting for both mobile and desktop data (optimized: 30s max)...")

        max_additional_wait = 30  # Reduced from 60 to 30 seconds
        wait_interval = 3  # Reduced from 5 to 3 seconds for more responsive checking
        elapsed = 0

        while elapsed < max_additional_wait:
            mobile_json = driver.execute_script("return window.__LIGHTHOUSE_MOBILE_JSON__;")
            desktop_json = driver.execute_script("return window.__LIGHTHOUSE_DESKTOP_JSON__;")

            if mobile_json and desktop_json:
                print("✅ Both mobile and desktop JSON data are available!")
                break
            elif mobile_json:
                print(f"📱 Mobile data ready, waiting for desktop data... ({elapsed}s)")
            elif desktop_json:
                print(f"💻 Desktop data ready, waiting for mobile data... ({elapsed}s)")
            else:
                print(f"⏳ Waiting for data... ({elapsed}s)")

            time.sleep(wait_interval)
            elapsed += wait_interval

        print("🔍 Extracting available results...")

        # Capture screenshots before extracting data (optimized for Full HD mobile and desktop)
        capture_full_hd_screenshots(driver, url_to_test, current_index, enable_screenshots)

        # Get the final URL (remove query parameters)
        final_url = driver.current_url.split("?")[0]
        print(f"Final URL: {final_url}")

        # Create result dictionary
        result = {"url": url_to_test, "final_url": final_url}

        # Extract mobile data
        mobile_json = driver.execute_script("return window.__LIGHTHOUSE_MOBILE_JSON__;")
        mobile_data = None
        if mobile_json:
            print("📱 Extracting mobile scores and metrics...")
            mobile_data = extract_lighthouse_data(mobile_json, "mobile")
            # Remove display data before updating result (keep it separate for table display)
            mobile_data_clean = {k: v for k, v in mobile_data.items() if not k.startswith('_')}
            result.update(mobile_data_clean)
        else:
            print("⚠️  Mobile JSON data not available")

        # Extract desktop data
        desktop_json = driver.execute_script("return window.__LIGHTHOUSE_DESKTOP_JSON__;")
        desktop_data = None
        if desktop_json:
            print("💻 Extracting desktop scores and metrics...")
            desktop_data = extract_lighthouse_data(desktop_json, "desktop")
            # Remove display data before updating result (keep it separate for table display)
            desktop_data_clean = {k: v for k, v in desktop_data.items() if not k.startswith('_')}
            result.update(desktop_data_clean)
        else:
            print("⚠️  Desktop JSON data not available")

        # Display results in table format
        if mobile_data or desktop_data:
            display_performance_table(mobile_data, desktop_data)

        return result

    except Exception as e:
        print(f"An error occurred during the test for {url_to_test}: {e}")
        return None
    finally:
        # Close the browser window
        driver.quit()
        print(f"Browser closed for URL: {url_to_test}")


def extract_lighthouse_data(lighthouse_json, device_type):
    """
    Extract scores and metrics from Lighthouse JSON data.
    Args:
        lighthouse_json: The Lighthouse JSON object
        device_type: String indicating "mobile" or "desktop"
    Returns:
        dict: Dictionary with scores and metrics for the specific device type
    """
    data = {}
    display_data = {}  # Separate data structure for table display

    try:
        # Extract category scores (Performance, Accessibility, Best Practices, SEO)
        categories = lighthouse_json.get('categories', {})

        for category_key, category_data in categories.items():
            category_name = category_data.get('title', category_key).lower().replace(' ', '_')
            category_title = category_data.get('title', category_key)
            score = category_data.get('score')
            if score is not None:
                # Convert score from 0-1 scale to 0-100 scale
                score_value = int(score * 100)
                data[f"{device_type}_{category_name}"] = score_value
                display_data[category_title] = score_value

        # Extract Core Web Vitals and other metrics
        audits = lighthouse_json.get('audits', {})

        # Define the metrics we want to extract
        metrics_mapping = {
            'first-contentful-paint': ('First Contentful Paint', 'first_contentful_paint'),
            'largest-contentful-paint': ('Largest Contentful Paint', 'largest_contentful_paint'),
            'total-blocking-time': ('Total Blocking Time', 'total_blocking_time'),
            'cumulative-layout-shift': ('Cumulative Layout Shift', 'cumulative_layout_shift'),
            'speed-index': ('Speed Index', 'speed_index'),
            'interactive': ('Time to Interactive', 'time_to_interactive'),
            'first-meaningful-paint': ('First Meaningful Paint', 'first_meaningful_paint')
        }

        for audit_key, (metric_display_name, metric_name) in metrics_mapping.items():
            audit = audits.get(audit_key, {})
            if audit:
                display_value = audit.get('displayValue', '')
                numeric_value = audit.get('numericValue')

                # Use display value if available, otherwise format numeric value
                if display_value:
                    value = display_value
                elif numeric_value is not None:
                    # Format based on the metric type
                    if audit_key == 'cumulative-layout-shift':
                        value = f"{numeric_value:.3f}"
                    elif 'paint' in audit_key or 'interactive' in audit_key or 'blocking' in audit_key or 'index' in audit_key:
                        # Time-based metrics - convert to seconds or milliseconds
                        if numeric_value >= 1000:
                            value = f"{numeric_value/1000:.2f} s"
                        else:
                            value = f"{numeric_value:.0f} ms"
                    else:
                        value = str(numeric_value)
                else:
                    continue

                data[f"{device_type}_{metric_name}"] = value
                display_data[metric_display_name] = value

    except Exception as e:
        print(f"Error extracting {device_type} data from Lighthouse JSON: {e}")

    # Store display data for table formatting
    data['_display_data'] = display_data
    data['_device_type'] = device_type

    return data

def display_performance_table(mobile_data, desktop_data):
    """
    Display performance metrics in a formatted table
    """
    # Extract display data
    mobile_display = mobile_data.get('_display_data', {}) if mobile_data else {}
    desktop_display = desktop_data.get('_display_data', {}) if desktop_data else {}

    # Combine all unique metrics
    all_metrics = set(mobile_display.keys()) | set(desktop_display.keys())

    if not all_metrics:
        print("⚠️  No performance data available for table display")
        return

    # Define the order of metrics for better organization
    metric_order = [
        'Performance', 'Accessibility', 'Best Practices', 'SEO',
        'First Contentful Paint', 'Largest Contentful Paint',
        'Total Blocking Time', 'Cumulative Layout Shift',
        'Speed Index', 'Time to Interactive', 'First Meaningful Paint'
    ]

    # Sort metrics by defined order, with unknown metrics at the end
    ordered_metrics = []
    for metric in metric_order:
        if metric in all_metrics:
            ordered_metrics.append(metric)

    # Add any remaining metrics not in the predefined order
    for metric in sorted(all_metrics):
        if metric not in ordered_metrics:
            ordered_metrics.append(metric)

    # Calculate column widths
    metric_width = max(len(metric) for metric in ordered_metrics) + 2
    mobile_width = max(len(str(mobile_display.get(metric, 'N/A'))) for metric in ordered_metrics) + 2
    desktop_width = max(len(str(desktop_display.get(metric, 'N/A'))) for metric in ordered_metrics) + 2

    # Ensure minimum widths for headers
    metric_width = max(metric_width, 25)
    mobile_width = max(mobile_width, 12)
    desktop_width = max(desktop_width, 12)

    # Print table header
    print(f"\n📊 Performance Metrics Summary")
    print("=" * (metric_width + mobile_width + desktop_width + 6))
    print(f"{'Metric':<{metric_width}} | {'📱 Mobile':<{mobile_width}} | {'🖥️  Desktop':<{desktop_width}}")
    print("=" * (metric_width + mobile_width + desktop_width + 6))

    # Print metrics rows
    for metric in ordered_metrics:
        mobile_value = mobile_display.get(metric, 'N/A')
        desktop_value = desktop_display.get(metric, 'N/A')

        # Add color coding for scores (if they're numeric)
        mobile_display_value = format_metric_value(mobile_value)
        desktop_display_value = format_metric_value(desktop_value)

        print(f"{metric:<{metric_width}} | {mobile_display_value:<{mobile_width}} | {desktop_display_value:<{desktop_width}}")

    print("=" * (metric_width + mobile_width + desktop_width + 6))
    print()

def format_metric_value(value):
    """
    Format metric values with color coding for scores
    """
    if str(value).isdigit():
        score = int(value)
        if score >= 90:
            return f"{value} ✅"  # Good
        elif score >= 50:
            return f"{value} ⚠️"   # Needs improvement
        else:
            return f"{value} ❌"   # Poor
    else:
        return str(value)

def write_to_csv(data, filename="pagespeed_results.csv"):
    """
    Writes a dictionary of results to a CSV file with structured columns.
    Args:
        data (dict): The dictionary containing the results.
        filename (str): The name of the CSV file to write to.
    """
    if not data:
        print("No data to write to CSV.")
        return

    # Create a clean copy of data excluding internal fields
    clean_data = {k: v for k, v in data.items() if not k.startswith('_')}

    # Define structured fieldnames for better CSV organization (original clean format)
    fieldnames = [
        "url",
        "final_url",
        # Mobile scores
        "mobile_performance",
        "mobile_accessibility",
        "mobile_best_practices",
        "mobile_seo",
        # Desktop scores
        "desktop_performance",
        "desktop_accessibility",
        "desktop_best_practices",
        "desktop_seo",
        # Mobile metrics
        "mobile_first_contentful_paint",
        "mobile_largest_contentful_paint",
        "mobile_total_blocking_time",
        "mobile_cumulative_layout_shift",
        "mobile_speed_index",
        "mobile_time_to_interactive",
        "mobile_first_meaningful_paint",
        # Desktop metrics
        "desktop_first_contentful_paint",
        "desktop_largest_contentful_paint",
        "desktop_total_blocking_time",
        "desktop_cumulative_layout_shift",
        "desktop_speed_index",
        "desktop_time_to_interactive",
        "desktop_first_meaningful_paint",
    ]

    # Add any additional fields found in the clean data that aren't in our standard list
    # (excluding internal fields that start with underscore)
    for key in clean_data.keys():
        if key not in fieldnames:
            fieldnames.append(key)

    # Check if the file exists to decide whether to write headers
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Open the CSV file in append mode and write the data
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

        # Write the header row only if the file is new
        if not file_exists:
            writer.writeheader()
            print(f"Created new CSV file with headers: {filename}")

        # Write the clean data row (without internal fields)
        writer.writerow(clean_data)

    print(f"Results for {clean_data.get('url', 'N/A')} successfully written to {filename}")





def read_urls_from_file(filename="urls.txt"):
    """
    Read URLs from a text file, one URL per line.
    Ignores blank lines, comments, and validates URL format.
    Args:
        filename (str): The name of the text file containing URLs.
    Returns:
        list: A list of valid URLs, with empty lines and invalid URLs filtered out.
    """
    try:
        urls = []
        invalid_lines = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
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
                    urls.append(clean_line)
                else:
                    invalid_lines.append(f"Line {line_num}: '{clean_line}' (invalid URL format)")

        # Report results
        if urls:
            print(f"✅ Successfully loaded {len(urls)} valid URLs from {filename}")
            if invalid_lines:
                print(f"⚠️  Skipped {len(invalid_lines)} invalid lines:")
                for invalid in invalid_lines:
                    print(f"   {invalid}")
        else:
            print(f"❌ No valid URLs found in {filename}")

        return urls

    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("Please create a 'urls.txt' file with URLs (one per line) or specify a different filename.")
        return []
    except Exception as e:
        print(f"❌ Error reading file '{filename}': {e}")
        return []

if __name__ == "__main__":
    # Read URLs from external file
    test_urls = read_urls_from_file("urls.txt")

    if not test_urls:
        print("No URLs found to test. Exiting.")
        exit(1)

    # Ask user if they want screenshot capture
    response = input("📸 Enable screenshot capture? (Y/n): ").lower().strip()
    enable_screenshots = response != 'n'

    if enable_screenshots:
        print(f"📸 Screenshots will be saved to a timestamped directory")

    print(f"🚀 Starting Lighthouse analysis for {len(test_urls)} URLs...")
    print("=" * 60)

    for i, url in enumerate(test_urls, 1):
        # Get the lighthouse results for each URL with progress tracking and optional screenshots
        page_speed_scores = get_pagespeed_results(url, i, len(test_urls), enable_screenshots)
        # Write the results to a CSV file
        if page_speed_scores:
            # Write main scores
            write_to_csv(page_speed_scores)
            print(f"✅ Successfully processed: {url}")
        else:
            print(f"❌ Failed to process: {url}")

        # Add a delay between tests to avoid being flagged as a bot
        if i < len(test_urls):  # Don't delay after the last URL
            delay = random.randint(5, 10)
            print(f"⏳ Waiting {delay} seconds before next test...")
            time.sleep(delay)

    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("📊 Generated files:")
    print("  • pagespeed_results.csv - Core performance metrics and scores")

    # Show screenshot summary if enabled
    if enable_screenshots and SCREENSHOT_DIR and os.path.exists(SCREENSHOT_DIR):
        screenshots = [f for f in os.listdir(SCREENSHOT_DIR) if f.endswith('.png')]
        if screenshots:
            print(f"  📸 {SCREENSHOT_DIR}/ - Screenshots ({len(screenshots)} files)")
            mobile_screenshots = [f for f in screenshots if f.startswith('fullhd_mobile_')]
            desktop_screenshots = [f for f in screenshots if f.startswith('fullhd_desktop_')]
            print(f"    📱 Mobile: {len(mobile_screenshots)} | 🖥️  Desktop: {len(desktop_screenshots)}")
        else:
            print("  ⚠️  No screenshots were captured")
