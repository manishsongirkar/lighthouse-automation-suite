# JSON-Based Lighthouse Data Extraction

## Overview

This updated version of the Lighthouse Automation Suite extracts data directly from the Lighthouse JSON objects instead of parsing HTML elements. This approach is more reliable and efficient.

## Key Changes

### Before (HTML Selector Approach)
- Used CSS selectors to find HTML elements (`div[aria-labelledby='mobile_tab']`, `.lh-scores-wrapper`, etc.)
- Required clicking between mobile/desktop tabs
- Fragile - breaks if PageSpeed Insights changes their HTML structure
- Complex element traversal and text extraction

### After (JSON-Based Approach)
- Extracts data directly from `window.__LIGHTHOUSE_MOBILE_JSON__` and `window.__LIGHTHOUSE_DESKTOP_JSON__` objects
- No need to interact with UI elements
- More reliable - JSON structure is more stable than HTML
- Access to complete Lighthouse audit data

## Benefits

1. **Reliability**: JSON structure is less likely to change compared to HTML/CSS
2. **Performance**: No need to wait for DOM elements or click between tabs
3. **Accuracy**: Direct access to Lighthouse audit results
4. **Completeness**: Access to all available metrics, not just what's displayed in UI
5. **Maintainability**: Less complex code, easier to debug

## Data Extracted

### Category Scores (0-100)
- Performance
- Accessibility
- Best Practices
- SEO

### Core Web Vitals & Metrics
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Total Blocking Time (TBT)
- Cumulative Layout Shift (CLS)
- Speed Index
- Time to Interactive (TTI)
- First Meaningful Paint (FMP)

## Usage

### Basic Usage
```python
from main import get_pagespeed_results

result = get_pagespeed_results("https://example.com")
print(result)
```

### Debug Mode
```python
# Enable debug mode to save raw JSON files
result = get_pagespeed_results("https://example.com", debug=True)
```

### Example Output
```python
{
    'url': 'https://example.com',
    'final_url': 'https://pagespeed.web.dev/analysis',
    'mobile_performance': 85,
    'mobile_accessibility': 95,
    'mobile_best_practices': 92,
    'mobile_seo': 90,
    'desktop_performance': 92,
    'desktop_accessibility': 95,
    'desktop_best_practices': 92,
    'desktop_seo': 90,
    'mobile_first_contentful_paint': '1.2 s',
    'mobile_largest_contentful_paint': '2.5 s',
    'mobile_total_blocking_time': '150 ms',
    'mobile_cumulative_layout_shift': '0.045',
    'mobile_speed_index': '2.8 s',
    'desktop_first_contentful_paint': '0.8 s',
    'desktop_largest_contentful_paint': '1.5 s',
    'desktop_total_blocking_time': '45 ms',
    'desktop_cumulative_layout_shift': '0.012',
    'desktop_speed_index': '1.9 s'
}
```

## Files

- `main.py` - Updated main script with JSON-based extraction
- `main_backup.py` - Backup of original HTML selector-based approach
- `main_json_debug.py` - Version with enhanced debugging capabilities
- `test_json_extraction.py` - Test script for validating the new approach

## Technical Details

### JSON Object Structure
The `window.__LIGHTHOUSE_MOBILE_JSON__` and `window.__LIGHTHOUSE_DESKTOP_JSON__` objects contain:

```javascript
{
  categories: {
    performance: { score: 0.85, title: "Performance" },
    accessibility: { score: 0.95, title: "Accessibility" },
    // ...
  },
  audits: {
    "first-contentful-paint": {
      displayValue: "1.2 s",
      numericValue: 1200,
      // ...
    },
    // ...
  }
}
```

### Wait Strategy
The script waits for either JSON object to become available:
```python
WebDriverWait(driver, 180).until(
    lambda driver: driver.execute_script(
        "return window.__LIGHTHOUSE_MOBILE_JSON__ || window.__LIGHTHOUSE_DESKTOP_JSON__;"
    )
)
```

## Migration Notes

If you're migrating from the old approach:

1. The new approach is a drop-in replacement
2. CSV output format includes additional metrics
3. Existing CSV files will continue to work (new columns will be appended)
4. Debug mode can help verify data accuracy during transition
