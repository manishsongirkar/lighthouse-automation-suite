import csv
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
def get_pagespeed_results(url_to_test, current_index=1, total_urls=1):
    """
    Gets Lighthouse scores by directly navigating to PageSpeed Insights analysis URL.
    Extracts both mobile and desktop scores from JSON objects.
    Args:
        url_to_test (str): The URL to be tested by Lighthouse via PageSpeed Insights.
        current_index (int): Current URL index being processed.
        total_urls (int): Total number of URLs to process.
    Returns:
        dict: A dictionary containing mobile scores, desktop scores, and final URL, or None if an error occurs.
    """
    progress_percent = (current_index / total_urls) * 100
    print("=" * 60)
    print(f"🔄 Processing URL {current_index}/{total_urls} ({progress_percent:.1f}%)")
    print(f"📊 Current URL: {url_to_test}")
    print("=" * 60)

    # --- Setup Selenium WebDriver with anti-bot measures ---
    options = webdriver.ChromeOptions()

    # Use a random user agent to mimic a real browser
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")

    # Privacy and clean browser settings
    options.add_argument("--incognito")  # Run in incognito/private mode
    options.add_argument("--disable-extensions")  # Disable all extensions
    options.add_argument("--disable-plugins")  # Disable plugins
    options.add_argument("--disable-default-apps")  # Disable default apps

    # Anti-bot detection measures
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Performance and security options
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-web-security")  # Disable web security
    options.add_argument("--allow-running-insecure-content")  # Allow mixed content

    # Run in headless mode for automation
    options.add_argument("--headless")  # Run in headless mode

    print("🔧 Chrome configured: Incognito mode, no extensions, optimized for analysis")

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
        print("Waiting for analysis to complete...")

        # Wait for the page to load and analysis to complete
        # We'll wait for either JSON object to be available first
        print("⏳ Waiting for Lighthouse JSON data to be available...")

        # Wait for at least one of the JSON objects to be available
        WebDriverWait(driver, 180).until(
            lambda driver: driver.execute_script(
                "return window.__LIGHTHOUSE_MOBILE_JSON__ || window.__LIGHTHOUSE_DESKTOP_JSON__;"
            )
        )

        print("✅ Initial Lighthouse JSON data detected.")

        # Now wait a bit more for both mobile and desktop data to be fully loaded
        print("⏳ Waiting for both mobile and desktop data to load...")

        # Check if both are available, if not wait a bit more
        max_additional_wait = 60  # seconds
        wait_interval = 5  # seconds
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

        # Get the final URL (remove query parameters)
        final_url = driver.current_url.split("?")[0]
        print(f"Final URL: {final_url}")

        # Create result dictionary
        result = {"url": url_to_test, "final_url": final_url}

        # Lists to collect additional insights
        all_opportunities = []
        all_accessibility_issues = []
        all_seo_details = []

        # Extract mobile data
        mobile_json = driver.execute_script("return window.__LIGHTHOUSE_MOBILE_JSON__;")
        if mobile_json:
            print("📱 Extracting mobile scores and metrics...")
            mobile_data = extract_lighthouse_data(mobile_json, "mobile")
            result.update(mobile_data)

            # Extract additional mobile insights
            mobile_opportunities = extract_performance_opportunities(mobile_json, "mobile", url_to_test)
            mobile_accessibility = extract_accessibility_issues(mobile_json, "mobile", url_to_test)
            mobile_seo = extract_seo_details(mobile_json, "mobile", url_to_test)

            all_opportunities.extend(mobile_opportunities)
            all_accessibility_issues.extend(mobile_accessibility)
            all_seo_details.extend(mobile_seo)

            print(f"  📊 Found {len(mobile_opportunities)} mobile optimization opportunities")
            print(f"  ♿ Found {len(mobile_accessibility)} mobile accessibility issues")
            print(f"  🔍 Found {len(mobile_seo)} mobile SEO details")
        else:
            print("⚠️  Mobile JSON data not available")

        # Extract desktop data
        desktop_json = driver.execute_script("return window.__LIGHTHOUSE_DESKTOP_JSON__;")
        if desktop_json:
            print("💻 Extracting desktop scores and metrics...")
            desktop_data = extract_lighthouse_data(desktop_json, "desktop")
            result.update(desktop_data)

            # Extract additional desktop insights
            desktop_opportunities = extract_performance_opportunities(desktop_json, "desktop", url_to_test)
            desktop_accessibility = extract_accessibility_issues(desktop_json, "desktop", url_to_test)
            desktop_seo = extract_seo_details(desktop_json, "desktop", url_to_test)

            all_opportunities.extend(desktop_opportunities)
            all_accessibility_issues.extend(desktop_accessibility)
            all_seo_details.extend(desktop_seo)

            print(f"  📊 Found {len(desktop_opportunities)} desktop optimization opportunities")
            print(f"  ♿ Found {len(desktop_accessibility)} desktop accessibility issues")
            print(f"  🔍 Found {len(desktop_seo)} desktop SEO details")
        else:
            print("⚠️  Desktop JSON data not available")

        # Store additional insights in result for potential use
        result['_opportunities'] = all_opportunities
        result['_accessibility_issues'] = all_accessibility_issues
        result['_seo_details'] = all_seo_details

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

    try:
        # Extract category scores (Performance, Accessibility, Best Practices, SEO)
        categories = lighthouse_json.get('categories', {})

        for category_key, category_data in categories.items():
            category_name = category_data.get('title', category_key).lower().replace(' ', '_')
            score = category_data.get('score')
            if score is not None:
                # Convert score from 0-1 scale to 0-100 scale
                score_value = int(score * 100)
                data[f"{device_type}_{category_name}"] = score_value
                print(f"  {device_type.title()} {category_data.get('title', category_key)}: {score_value}")

        # Extract Core Web Vitals and other metrics
        audits = lighthouse_json.get('audits', {})

        # Define the metrics we want to extract
        metrics_mapping = {
            'first-contentful-paint': 'first_contentful_paint',
            'largest-contentful-paint': 'largest_contentful_paint',
            'total-blocking-time': 'total_blocking_time',
            'cumulative-layout-shift': 'cumulative_layout_shift',
            'speed-index': 'speed_index',
            'interactive': 'time_to_interactive',
            'first-meaningful-paint': 'first_meaningful_paint'
        }

        for audit_key, metric_name in metrics_mapping.items():
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
                print(f"  {device_type.title()} {metric_name.replace('_', ' ').title()}: {value}")

    except Exception as e:
        print(f"Error extracting {device_type} data from Lighthouse JSON: {e}")

    return data


def extract_performance_opportunities(lighthouse_json, device_type, url):
    """
    Extract performance optimization opportunities from Lighthouse JSON.
    Args:
        lighthouse_json: The Lighthouse JSON object
        device_type: String indicating "mobile" or "desktop"
        url: The URL being analyzed
    Returns:
        list: List of opportunity dictionaries
    """
    opportunities = []

    try:
        audits = lighthouse_json.get('audits', {})

        # Key performance opportunity audits
        opportunity_audits = {
            'uses-optimized-images': 'Optimize images',
            'modern-image-formats': 'Use modern image formats',
            'unused-css-rules': 'Remove unused CSS',
            'render-blocking-resources': 'Eliminate render-blocking resources',
            'uses-text-compression': 'Enable text compression',
            'efficient-animated-content': 'Use efficient animated content',
            'uses-responsive-images': 'Use appropriately sized images',
            'offscreen-images': 'Defer offscreen images',
            'unminified-css': 'Minify CSS',
            'unminified-javascript': 'Minify JavaScript',
            'uses-http2': 'Use HTTP/2',
            'font-display': 'Ensure text remains visible during webfont load'
        }

        for audit_key, description in opportunity_audits.items():
            audit = audits.get(audit_key, {})
            if audit and audit.get('score') is not None and audit.get('score') < 1:
                potential_savings = audit.get('details', {}).get('overallSavingsMs', 0)
                if potential_savings > 0:
                    opportunities.append({
                        'url': url,
                        'device_type': device_type,
                        'audit_id': audit_key,
                        'title': audit.get('title', description),
                        'description': audit.get('description', ''),
                        'score': audit.get('score', 0),
                        'potential_savings_ms': potential_savings,
                        'potential_savings_s': f"{potential_savings/1000:.2f}",
                        'impact': 'High' if potential_savings > 1000 else 'Medium' if potential_savings > 500 else 'Low'
                    })

    except Exception as e:
        print(f"Error extracting opportunities for {device_type}: {e}")

    return opportunities


def extract_accessibility_issues(lighthouse_json, device_type, url):
    """
    Extract accessibility issues from Lighthouse JSON.
    Args:
        lighthouse_json: The Lighthouse JSON object
        device_type: String indicating "mobile" or "desktop"
        url: The URL being analyzed
    Returns:
        list: List of accessibility issue dictionaries
    """
    issues = []

    try:
        audits = lighthouse_json.get('audits', {})

        # Key accessibility audits
        accessibility_audits = {
            'color-contrast': 'Color contrast',
            'image-alt': 'Image alt text',
            'aria-labels': 'ARIA labels',
            'heading-order': 'Heading order',
            'link-name': 'Link names',
            'button-name': 'Button names',
            'form-field-multiple-labels': 'Form field labels',
            'skip-link': 'Skip links',
            'tabindex': 'Tab index usage',
            'focus-traps': 'Focus traps'
        }

        for audit_key, description in accessibility_audits.items():
            audit = audits.get(audit_key, {})
            if audit and audit.get('score') is not None and audit.get('score') < 1:
                severity = 'Critical' if audit.get('score') == 0 else 'Warning'
                issues.append({
                    'url': url,
                    'device_type': device_type,
                    'audit_id': audit_key,
                    'title': audit.get('title', description),
                    'description': audit.get('description', ''),
                    'score': audit.get('score', 0),
                    'severity': severity,
                    'impact': audit.get('details', {}).get('type', 'Unknown')
                })

    except Exception as e:
        print(f"Error extracting accessibility issues for {device_type}: {e}")

    return issues


def extract_seo_details(lighthouse_json, device_type, url):
    """
    Extract SEO details from Lighthouse JSON.
    Args:
        lighthouse_json: The Lighthouse JSON object
        device_type: String indicating "mobile" or "desktop"
        url: The URL being analyzed
    Returns:
        list: List of SEO issue dictionaries
    """
    seo_details = []

    try:
        audits = lighthouse_json.get('audits', {})

        # Key SEO audits
        seo_audits = {
            'meta-description': 'Meta description',
            'document-title': 'Document title',
            'structured-data': 'Structured data',
            'robots-txt': 'Robots.txt',
            'canonical': 'Canonical links',
            'hreflang': 'Hreflang',
            'is-crawlable': 'Page is crawlable',
            'font-size': 'Font size',
            'tap-targets': 'Tap targets'
        }

        for audit_key, description in seo_audits.items():
            audit = audits.get(audit_key, {})
            if audit:
                status = 'Pass' if audit.get('score', 0) == 1 else 'Fail' if audit.get('score', 0) == 0 else 'Warning'
                seo_details.append({
                    'url': url,
                    'device_type': device_type,
                    'audit_id': audit_key,
                    'title': audit.get('title', description),
                    'description': audit.get('description', ''),
                    'score': audit.get('score', 0),
                    'status': status,
                    'displayValue': audit.get('displayValue', '')
                })

    except Exception as e:
        print(f"Error extracting SEO details for {device_type}: {e}")

    return seo_details

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


def write_opportunities_to_csv(opportunities, filename="lighthouse_opportunities.csv"):
    """
    Writes performance opportunities to a separate CSV file.
    Args:
        opportunities (list): List of opportunity dictionaries.
        filename (str): The name of the CSV file to write to.
    """
    if not opportunities:
        return

    fieldnames = [
        "url", "device_type", "audit_id", "title", "description",
        "score", "potential_savings_ms", "potential_savings_s", "impact"
    ]

    # Check if file exists
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Write data
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            print(f"Created opportunities CSV: {filename}")
        for opportunity in opportunities:
            writer.writerow(opportunity)


def write_accessibility_to_csv(issues, filename="lighthouse_accessibility.csv"):
    """
    Writes accessibility issues to a separate CSV file.
    Args:
        issues (list): List of accessibility issue dictionaries.
        filename (str): The name of the CSV file to write to.
    """
    if not issues:
        return

    fieldnames = [
        "url", "device_type", "audit_id", "title", "description",
        "score", "severity", "impact"
    ]

    # Check if file exists
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Write data
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            print(f"Created accessibility CSV: {filename}")
        for issue in issues:
            writer.writerow(issue)


def write_seo_to_csv(seo_details, filename="lighthouse_seo_details.csv"):
    """
    Writes SEO details to a separate CSV file.
    Args:
        seo_details (list): List of SEO detail dictionaries.
        filename (str): The name of the CSV file to write to.
    """
    if not seo_details:
        return

    fieldnames = [
        "url", "device_type", "audit_id", "title", "description",
        "score", "status", "displayValue"
    ]

    # Check if file exists
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Write data
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            print(f"Created SEO details CSV: {filename}")
        for detail in seo_details:
            writer.writerow(detail)

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

    print(f"Starting Lighthouse analysis for {len(test_urls)} URLs...")
    print("=" * 60)

    for i, url in enumerate(test_urls, 1):
        # Get the lighthouse results for each URL with progress tracking
        page_speed_scores = get_pagespeed_results(url, i, len(test_urls))
        # Write the results to a CSV file
        if page_speed_scores:
            # Write main scores (existing format)
            write_to_csv(page_speed_scores)

            # Write additional insights to separate CSV files
            if '_opportunities' in page_speed_scores:
                write_opportunities_to_csv(page_speed_scores['_opportunities'])
            if '_accessibility_issues' in page_speed_scores:
                write_accessibility_to_csv(page_speed_scores['_accessibility_issues'])
            if '_seo_details' in page_speed_scores:
                write_seo_to_csv(page_speed_scores['_seo_details'])

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
    print("  • pagespeed_results.csv - Main scores and metrics")
    print("  • lighthouse_opportunities.csv - Performance optimization opportunities")
    print("  • lighthouse_accessibility.csv - Accessibility issues and recommendations")
    print("  • lighthouse_seo_details.csv - SEO audit details")
