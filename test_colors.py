import pandas as pd
import re

def get_metric_class(value, metric_type):
    """
    Determine CSS class based on Core Web Vitals thresholds
    """
    if pd.isna(value) or value == 'N/A':
        return 'metric-na'

    # Handle string values with units
    if isinstance(value, str):
        # Extract numeric value from strings like '1.2 s', '450 ms'
        numeric_match = re.search(r'(\d+\.?\d*)', value)
        if numeric_match:
            numeric_value = float(numeric_match.group(1))
        else:
            return 'metric-na'
    else:
        numeric_value = float(value)

    # Core Web Vitals thresholds (Google standards)
    thresholds = {
        'fcp': {'good': 1.8, 'poor': 3.0},  # First Contentful Paint (seconds)
        'lcp': {'good': 2.5, 'poor': 4.0},  # Largest Contentful Paint (seconds)
        'tbt': {'good': 200, 'poor': 600},  # Total Blocking Time (ms)
        'cls': {'good': 0.1, 'poor': 0.25}, # Cumulative Layout Shift
        'si': {'good': 3.4, 'poor': 5.8},   # Speed Index (seconds)
        'performance': {'good': 90, 'poor': 50}  # Performance score
    }

    if metric_type in thresholds:
        threshold = thresholds[metric_type]
        if numeric_value <= threshold['good']:
            return 'metric-good'
        elif numeric_value <= threshold['poor']:
            return 'metric-needs-improvement'
        else:
            return 'metric-poor'

    return 'metric-default'

# Test the color coding function
print('Testing color coding function:')
print(f'FCP 1.2s: {get_metric_class("1.2 s", "fcp")}')
print(f'LCP 5.2s: {get_metric_class("5.2 s", "lcp")}')
print(f'Performance 85: {get_metric_class(85, "performance")}')
print(f'Performance 45: {get_metric_class(45, "performance")}')
print(f'TBT 450ms: {get_metric_class("450 ms", "tbt")}')
print(f'CLS 0.15: {get_metric_class(0.15, "cls")}')
