import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
def get_pagespeed_results(url_to_test, current_index=1, total_urls=1):
    """
    Gets PageSpeed Insights scores by directly navigating to analysis URL.
    Extracts both mobile and desktop scores separately.
    Args:
        url_to_test (str): The URL to be tested by PageSpeed Insights.
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
        # STEP 1: Wait for mobile tab div and process mobile scores
        print("STEP 1: Processing Mobile Tab...")
        print("Waiting for mobile tab div...")
        mobile_tab_div = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-labelledby='mobile_tab']")
            )
        )
        print("Waiting for mobile score wrapper...")
        mobile_score_wrapper = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[aria-labelledby='mobile_tab'] .lh-scores-wrapper",
                )
            )
        )

        mobile_metrics_wrapper = WebDriverWait(driver, 5).until( EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "div[aria-labelledby='mobile_tab'] .lh-metrics-container",
            )
        ) )

        print(":white_check_mark: Mobile score wrapper loaded. Extracting mobile scores...")
        # Get the final URL (remove query parameters)
        final_url = driver.current_url.split("?")[0]
        print(f"Final URL: {final_url}")
        # Create result dictionary
        result = {"url": url_to_test, "final_url": final_url}
        # Extract mobile scores
        mobile_scores = extract_scores_from_wrapper(mobile_score_wrapper, "mobile")
        mobile_metrics = extract_metrics_from_wrapper(mobile_metrics_wrapper, "mobile")

        result.update(mobile_scores)
        result.update(mobile_metrics)
        # STEP 2: Now click desktop tab and process desktop scores
        print("\nSTEP 2: Processing Desktop Tab...")
        # Find and click the desktop tab button
        print("Looking for tab buttons container...")
        tab_container = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[jsshadow][data-use-automatic-activation='false']",
                )
            )
        )
        print("Finding tab buttons...")
        tab_buttons = tab_container.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(tab_buttons)} tab buttons")
        if len(tab_buttons) >= 2:
            # Click the second button (desktop tab)
            desktop_button = tab_buttons[1]
            print("Clicking desktop tab button...")
            driver.execute_script("arguments[0].click();", desktop_button)
            print(":white_check_mark: Desktop tab button clicked")
            time.sleep(3)  # Wait for tab to activate
        else:
            print(":warning: Could not find desktop tab button")
            return result  # Return with mobile data only
        # Wait for desktop tab div to appear
        print("Waiting for desktop tab div...")
        desktop_tab_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-labelledby='desktop_tab']")
            )
        )
        print("Waiting for desktop score wrapper...")
        desktop_score_wrapper = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[aria-labelledby='desktop_tab'] .lh-scores-wrapper",
                )
            )
        )

        desktop_metrics_wrapper = WebDriverWait(driver, 5).until( EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "div[aria-labelledby='desktop_tab'] .lh-metrics-container",
            )
        ) )
        print(":white_check_mark: Desktop score wrapper loaded. Extracting desktop scores...")
        # Extract desktop scores
        desktop_scores = extract_scores_from_wrapper(desktop_score_wrapper, "desktop")
        desktop_metrics = extract_metrics_from_wrapper(desktop_metrics_wrapper, "desktop")
        result.update(desktop_scores)
        result.update(desktop_metrics)
        return result
    except Exception as e:
        print(f"An error occurred during the test for {url_to_test}: {e}")
        return None
    finally:
        # Close the browser window
        driver.quit()
        print(f"Browser closed for URL: {url_to_test}")

def extract_metrics_from_wrapper(metrics_wrapper, device_type):
    metrics = {}
    selectors = [
        '#first-contentful-paint',
        '#largest-contentful-paint',
        '#total-blocking-time',
        '#cumulative-layout-shift',
        '#speed-index'
    ]
    try:
        for i in selectors:
            label = metrics_wrapper.find_element( By.CSS_SELECTOR, f"{i} .lh-metric__title" )
            label = label.text
            label = label.replace( ' ', '_' )
            label = label.lower()
            value = metrics_wrapper.find_element( By.CSS_SELECTOR, f"{i} .lh-metric__value" )
            metrics[ f"{device_type}_{label}" ] = value.text
    except Exception as e:
        print(f"Error processing {device_type} metrics wrapper: {e}")

    return metrics

def extract_scores_from_wrapper(score_wrapper, device_type):
    """
    Extract scores from a specific score wrapper element (mobile or desktop).
    Args:
        score_wrapper: The selenium web element for the lh-scores-wrapper
        device_type: String indicating "mobile" or "desktop"
    Returns:
        dict: Dictionary with scores for the specific device type
    """
    scores = {}
    try:
        # Find all gauge wrappers within this score wrapper
        gauge_wrappers = score_wrapper.find_elements(By.CLASS_NAME, "lh-gauge__wrapper")
        print(
            f"Found {len(gauge_wrappers)} gauge wrappers in {device_type} score wrapper"
        )
        # Extract data from each gauge wrapper
        for i, gauge_wrapper in enumerate(gauge_wrappers):
            try:
                # Get all child elements of the gauge wrapper
                child_elements = gauge_wrapper.find_elements(By.XPATH, "./*")
                # Extract text from the last 2 children
                if len(child_elements) >= 2:
                    score_text = child_elements[-2].text.strip()
                    label_text = child_elements[-1].text.strip()
                    print(
                        f"{device_type.title()} Gauge {i+1} - Score: {score_text}, Label: {label_text}"
                    )
                    # Add to scores dictionary using device type prefix
                    if label_text and score_text:
                        # Clean up label to use as dictionary key
                        key = label_text.lower().replace(" ", "_")
                        scores[f"{device_type}_{key}"] = score_text
                else:
                    print(
                        f"{device_type.title()} Gauge {i+1} - Could not find enough child elements"
                    )
            except Exception as e:
                print(f"Error extracting data from {device_type} gauge {i+1}: {e}")
                continue
    except Exception as e:
        print(f"Error processing {device_type} score wrapper: {e}")
    return scores
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
    # Define structured fieldnames for better CSV organization
    fieldnames = [
        "url",
        "final_url",
        "mobile_performance",
        "mobile_accessibility",
        "mobile_best_practices",
        "mobile_seo",
        "desktop_performance",
        "desktop_accessibility",
        "desktop_best_practices",
        "desktop_seo",
    ]
    # Add any additional fields found in the data that aren't in our standard list
    for key in data.keys():
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
        # Write the data row
        writer.writerow(data)
    print(f"Results for {data.get('url', 'N/A')} successfully written to {filename}")

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

    print(f"Starting PageSpeed analysis for {len(test_urls)} URLs...")
    print("=" * 60)

    for i, url in enumerate(test_urls, 1):
        # Get the pagespeed results for each URL with progress tracking
        page_speed_scores = get_pagespeed_results(url, i, len(test_urls))
        # Write the results to a CSV file
        if page_speed_scores:
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
    print("Check 'pagespeed_results.csv' for results.")
