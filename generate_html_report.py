#!/usr/bin/env python3
"""
HTML Report Generator for Lighthouse Results
Generates a color-coded HTML dashboard from CSV results
"""
import csv
import pandas as pd
from datetime import datetime

def generate_html_report(csv_file="pagespeed_results.csv", html_file="pagespeed_report.html"):
    """Generate an HTML dashboard report"""
    try:
        df = pd.read_csv(csv_file)

        # Debug: Check for duplicates and remove them
        initial_count = len(df)
        df = df.drop_duplicates(subset=['url'], keep='first')
        final_count = len(df)

        if initial_count != final_count:
            print(f"⚠️  Warning: Removed {initial_count - final_count} duplicate URLs from data")
            print(f"   Original count: {initial_count}, After deduplication: {final_count}")

        print(f"📊 Processing {len(df)} unique URLs for HTML report")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lighthouse Automation Suite Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #1a73e8; margin: 0; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0 0 10px 0; }}
        .summary-card .number {{ font-size: 2em; font-weight: bold; }}
        .results-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .results-table th, .results-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        .results-table th {{ background-color: #f8f9fa; font-weight: 600; }}
        .score {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; color: white; text-align: center; }}
        .score-good {{ background: #0f9d58; }}
        .score-average {{ background: #ff9800; }}
        .score-poor {{ background: #f44336; }}
        .url-cell {{ max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .metrics-section {{ margin-top: 30px; }}
        .device-section {{ margin: 20px 0; }}
        .device-title {{ font-size: 1.2em; font-weight: bold; color: #333; margin-bottom: 10px; }}
        .vitals-section {{ margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .vitals-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
        .vitals-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .vitals-card h4 {{ margin: 0 0 15px 0; color: #333; font-size: 1.1em; }}
        .metric-item {{ display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px; background: #f5f5f5; border-radius: 4px; }}
        .metric-name {{ font-weight: 500; }}
        .metric-value {{ font-family: monospace; font-weight: bold; padding: 4px 8px; border-radius: 4px; color: white; }}
        .metric-good {{ background: #0f9d58; }}
        .metric-needs-improvement {{ background: #ff9800; }}
        .metric-poor {{ background: #f44336; }}
        .metric-neutral {{ background: #666; color: white; }}
        .section-divider {{ border: none; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 40px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Lighthouse Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p style="color: #666; font-size: 0.9em;">
                📈 Analyzing <strong>{len(df)} unique URLs</strong> •
                Each URL appears in 3 sections: Mobile Scores, Desktop Scores, and Core Web Vitals •
                📊 Click "View Report" links to open the full Lighthouse analysis via PageSpeed Insights
            </p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <h3>URLs Analyzed</h3>
                <div class="number">{len(df)}</div>
            </div>
            <div class="summary-card">
                <h3>Avg Mobile Performance</h3>
                <div class="number">{df['mobile_performance'].mean():.0f}</div>
            </div>
            <div class="summary-card">
                <h3>Avg Desktop Performance</h3>
                <div class="number">{df['desktop_performance'].mean():.0f}</div>
            </div>
            <div class="summary-card">
                <h3>Overall Health</h3>
                <div class="number">{((df['mobile_performance'].mean() + df['desktop_performance'].mean()) / 2):.0f}</div>
            </div>
        </div>

        <!-- Core Web Vitals Summary -->
        <div class="summary" style="margin-top: 20px;">"""

        # Add Core Web Vitals summary cards if data exists
        vitals_summary = ""

        # Check for mobile LCP (Largest Contentful Paint) as a key metric
        if 'mobile_largest_contentful_paint' in df.columns:
            # Calculate average mobile LCP (remove 's' suffix and convert to float)
            mobile_lcp_values = df['mobile_largest_contentful_paint'].apply(lambda x: float(str(x).replace('s', '').replace(',', '').strip()) if pd.notna(x) else 0)
            avg_mobile_lcp = mobile_lcp_values.mean()
            card_style = get_summary_card_style("lcp", avg_mobile_lcp)
            vitals_summary += f"""
            <div class="summary-card" style="{card_style}">
                <h3>Avg Mobile LCP</h3>
                <div class="number" style="font-size: 1.5em;">{avg_mobile_lcp:.1f}s</div>
            </div>"""

        # Check for desktop LCP
        if 'desktop_largest_contentful_paint' in df.columns:
            desktop_lcp_values = df['desktop_largest_contentful_paint'].apply(lambda x: float(str(x).replace('s', '').replace(',', '').strip()) if pd.notna(x) else 0)
            avg_desktop_lcp = desktop_lcp_values.mean()
            card_style = get_summary_card_style("lcp", avg_desktop_lcp)
            vitals_summary += f"""
            <div class="summary-card" style="{card_style}">
                <h3>Avg Desktop LCP</h3>
                <div class="number" style="font-size: 1.5em;">{avg_desktop_lcp:.1f}s</div>
            </div>"""

        # Check for mobile CLS (Cumulative Layout Shift)
        if 'mobile_cumulative_layout_shift' in df.columns:
            mobile_cls_values = df['mobile_cumulative_layout_shift'].apply(lambda x: float(str(x)) if pd.notna(x) and str(x).replace('.','').isdigit() else 0)
            avg_mobile_cls = mobile_cls_values.mean()
            card_style = get_summary_card_style("cls", avg_mobile_cls)
            vitals_summary += f"""
            <div class="summary-card" style="{card_style}">
                <h3>Avg Mobile CLS</h3>
                <div class="number" style="font-size: 1.5em;">{avg_mobile_cls:.3f}</div>
            </div>"""

        # Check for desktop CLS
        if 'desktop_cumulative_layout_shift' in df.columns:
            desktop_cls_values = df['desktop_cumulative_layout_shift'].apply(lambda x: float(str(x)) if pd.notna(x) and str(x).replace('.','').isdigit() else 0)
            avg_desktop_cls = desktop_cls_values.mean()
            card_style = get_summary_card_style("cls", avg_desktop_cls)
            vitals_summary += f"""
            <div class="summary-card" style="{card_style}">
                <h3>Avg Desktop CLS</h3>
                <div class="number" style="font-size: 1.5em;">{avg_desktop_cls:.3f}</div>
            </div>"""

        html_content += vitals_summary + """
        </div>

        <div class="metrics-section">
            <h2>📱 Mobile Performance Scores</h2>
            <p style="color: #666; margin-bottom: 15px;">Performance scores for mobile devices</p>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Performance</th>
                        <th>Accessibility</th>
                        <th>Best Practices</th>
                        <th>SEO</th>
                        <th>Lighthouse Report</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Add mobile results
        for _, row in df.iterrows():
            pagespeed_url = row.get('final_url', '')
            pagespeed_link = f'<a href="{pagespeed_url}" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: 500;">📊 View Report</a>' if pagespeed_url else 'N/A'

            html_content += f"""
                    <tr>
                        <td class="url-cell" title="{row['url']}">{row['url']}</td>
                        <td><span class="score {get_score_class(row['mobile_performance'])}">{row['mobile_performance']}</span></td>
                        <td><span class="score {get_score_class(row['mobile_accessibility'])}">{row['mobile_accessibility']}</span></td>
                        <td><span class="score {get_score_class(row['mobile_best_practices'])}">{row['mobile_best_practices']}</span></td>
                        <td><span class="score {get_score_class(row['mobile_seo'])}">{row['mobile_seo']}</span></td>
                        <td>{pagespeed_link}</td>
                    </tr>
            """

        html_content += """
                </tbody>
            </table>

            <h2>🖥️ Desktop Performance Scores</h2>
            <p style="color: #666; margin-bottom: 15px;">Performance scores for desktop devices (same URLs as above)</p>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Performance</th>
                        <th>Accessibility</th>
                        <th>Best Practices</th>
                        <th>SEO</th>
                        <th>Lighthouse Report</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Add desktop results
        for _, row in df.iterrows():
            pagespeed_url = row.get('final_url', '')
            pagespeed_link = f'<a href="{pagespeed_url}" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: 500;">📊 View Report</a>' if pagespeed_url else 'N/A'

            html_content += f"""
                    <tr>
                        <td class="url-cell" title="{row['url']}">{row['url']}</td>
                        <td><span class="score {get_score_class(row['desktop_performance'])}">{row['desktop_performance']}</span></td>
                        <td><span class="score {get_score_class(row['desktop_accessibility'])}">{row['desktop_accessibility']}</span></td>
                        <td><span class="score {get_score_class(row['desktop_best_practices'])}">{row['desktop_best_practices']}</span></td>
                        <td><span class="score {get_score_class(row['desktop_seo'])}">{row['desktop_seo']}</span></td>
                        <td>{pagespeed_link}</td>
                    </tr>
            """

        html_content += """
                </tbody>
            </table>
        </div>

        <hr class="section-divider">

        <div class="vitals-section">
            <h2>⚡ Core Web Vitals & Performance Metrics</h2>
            <p>Detailed performance metrics for each analyzed URL (same URLs as above, with detailed timing data)</p>

            <div class="vitals-grid">
        """

        # Add Core Web Vitals for each URL
        for _, row in df.iterrows():
            # Check if Core Web Vitals columns exist
            mobile_metrics = {}
            desktop_metrics = {}

            # Core Web Vitals mapping
            metrics_mapping = {
                'mobile_first_contentful_paint': 'First Contentful Paint',
                'mobile_largest_contentful_paint': 'Largest Contentful Paint',
                'mobile_total_blocking_time': 'Total Blocking Time',
                'mobile_cumulative_layout_shift': 'Cumulative Layout Shift',
                'mobile_speed_index': 'Speed Index',
                'desktop_first_contentful_paint': 'First Contentful Paint',
                'desktop_largest_contentful_paint': 'Largest Contentful Paint',
                'desktop_total_blocking_time': 'Total Blocking Time',
                'desktop_cumulative_layout_shift': 'Cumulative Layout Shift',
                'desktop_speed_index': 'Speed Index'
            }

            # Collect available mobile metrics
            for col, display_name in metrics_mapping.items():
                if col in row and pd.notna(row[col]) and col.startswith('mobile_'):
                    mobile_metrics[display_name] = row[col]
                elif col in row and pd.notna(row[col]) and col.startswith('desktop_'):
                    desktop_metrics[display_name] = row[col]

            html_content += f"""
                <div class="vitals-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h4 style="margin: 0;">🌐 {row['url']}</h4>
                        {f'<a href="{row.get("final_url", "")}" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: 500; font-size: 0.9em;">📊 View Full Report</a>' if row.get('final_url') else ''}
                    </div>

                    <div style="margin-bottom: 20px;">
                        <strong>📱 Mobile Metrics:</strong>
            """

            if mobile_metrics:
                for metric_name, value in mobile_metrics.items():
                    # Get the original column name for threshold checking
                    col_name = f"mobile_{metric_name.lower().replace(' ', '_')}"
                    metric_class = get_metric_class(col_name, value)
                    html_content += f"""
                        <div class="metric-item">
                            <span class="metric-name">{metric_name}</span>
                            <span class="metric-value {metric_class}">{value}</span>
                        </div>
                    """
            else:
                html_content += '<p style="color: #666; font-style: italic;">No mobile metrics available</p>'

            html_content += """
                    </div>

                    <div>
                        <strong>🖥️ Desktop Metrics:</strong>
            """

            if desktop_metrics:
                for metric_name, value in desktop_metrics.items():
                    # Get the original column name for threshold checking
                    col_name = f"desktop_{metric_name.lower().replace(' ', '_')}"
                    metric_class = get_metric_class(col_name, value)
                    html_content += f"""
                        <div class="metric-item">
                            <span class="metric-name">{metric_name}</span>
                            <span class="metric-value {metric_class}">{value}</span>
                        </div>
                    """
            else:
                html_content += '<p style="color: #666; font-style: italic;">No desktop metrics available</p>'

            html_content += """
                    </div>
                </div>
            """

        html_content += """
            </div>
        </div>

        <hr class="section-divider">

        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center;">
            <p><strong>Performance Score Legend:</strong></p>
            <span class="score score-good">90-100 Good</span>
            <span class="score score-average">50-89 Needs Improvement</span>
            <span class="score score-poor">0-49 Poor</span>

            <div style="margin-top: 20px;">
                <p><strong>Core Web Vitals Color Legend:</strong></p>
                <div style="margin: 10px 0;">
                    <span class="metric-value metric-good" style="margin: 0 5px;">Good</span>
                    <span class="metric-value metric-needs-improvement" style="margin: 0 5px;">Needs Improvement</span>
                    <span class="metric-value metric-poor" style="margin: 0 5px;">Poor</span>
                </div>
            </div>

            <div style="margin-top: 20px;">
                <p><strong>Core Web Vitals Thresholds:</strong></p>
                <div style="font-size: 0.85em; color: #666; text-align: left; max-width: 600px; margin: 0 auto;">
                    <div style="margin: 5px 0;"><strong>FCP (First Contentful Paint):</strong> Good &lt;1.8s, Needs Improvement 1.8-3.0s, Poor &gt;3.0s</div>
                    <div style="margin: 5px 0;"><strong>LCP (Largest Contentful Paint):</strong> Good &lt;2.5s, Needs Improvement 2.5-4.0s, Poor &gt;4.0s</div>
                    <div style="margin: 5px 0;"><strong>TBT (Total Blocking Time):</strong> Good &lt;200ms, Needs Improvement 200-600ms, Poor &gt;600ms</div>
                    <div style="margin: 5px 0;"><strong>CLS (Cumulative Layout Shift):</strong> Good &lt;0.1, Needs Improvement 0.1-0.25, Poor &gt;0.25</div>
                    <div style="margin: 5px 0;"><strong>SI (Speed Index):</strong> Good &lt;3.4s, Needs Improvement 3.4-5.8s, Poor &gt;5.8s</div>
                </div>
            </div>
            </div>
        </div>
    </div>
</body>
</html>
        """

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML report generated: {html_file}")
        print(f"   Open in browser: file://{html_file}")

    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")

def get_summary_card_style(metric_type, value):
    """Return CSS style for summary cards based on performance thresholds"""
    if metric_type == "lcp":  # Largest Contentful Paint
        if value < 2.5:
            return "background: linear-gradient(135deg, #0f9d58 0%, #0d7c45 100%);"  # Green
        elif value < 4.0:
            return "background: linear-gradient(135deg, #ff9800 0%, #e68900 100%);"  # Orange
        else:
            return "background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);"  # Red
    elif metric_type == "cls":  # Cumulative Layout Shift
        if value < 0.1:
            return "background: linear-gradient(135deg, #0f9d58 0%, #0d7c45 100%);"  # Green
        elif value < 0.25:
            return "background: linear-gradient(135deg, #ff9800 0%, #e68900 100%);"  # Orange
        else:
            return "background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);"  # Red
    else:
        return "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"  # Default

def get_score_class(score):
    """Return CSS class based on score"""
    if score >= 90:
        return "score-good"
    elif score >= 50:
        return "score-average"
    else:
        return "score-poor"

def get_metric_class(metric_name, value_str):
    """Return CSS class based on Core Web Vitals thresholds"""
    try:
        # Clean the value string and convert to float
        clean_value = str(value_str).replace('s', '').replace('ms', '').replace(',', '').strip()
        if not clean_value or not clean_value.replace('.', '').replace('-', '').isdigit():
            return "metric-neutral"

        value = float(clean_value)

        # Core Web Vitals thresholds (Google standards)
        if 'first_contentful_paint' in metric_name.lower():
            # FCP: Good < 1.8s, Needs Improvement 1.8-3.0s, Poor > 3.0s
            if value < 1.8:
                return "metric-good"
            elif value < 3.0:
                return "metric-needs-improvement"
            else:
                return "metric-poor"

        elif 'largest_contentful_paint' in metric_name.lower():
            # LCP: Good < 2.5s, Needs Improvement 2.5-4.0s, Poor > 4.0s
            if value < 2.5:
                return "metric-good"
            elif value < 4.0:
                return "metric-needs-improvement"
            else:
                return "metric-poor"

        elif 'total_blocking_time' in metric_name.lower():
            # TBT: Good < 200ms, Needs Improvement 200-600ms, Poor > 600ms
            # Convert seconds to milliseconds if needed
            if 's' in str(value_str) and value < 10:  # Likely in seconds
                value = value * 1000
            if value < 200:
                return "metric-good"
            elif value < 600:
                return "metric-needs-improvement"
            else:
                return "metric-poor"

        elif 'cumulative_layout_shift' in metric_name.lower():
            # CLS: Good < 0.1, Needs Improvement 0.1-0.25, Poor > 0.25
            if value < 0.1:
                return "metric-good"
            elif value < 0.25:
                return "metric-needs-improvement"
            else:
                return "metric-poor"

        elif 'speed_index' in metric_name.lower():
            # Speed Index: Good < 3.4s, Needs Improvement 3.4-5.8s, Poor > 5.8s
            if value < 3.4:
                return "metric-good"
            elif value < 5.8:
                return "metric-needs-improvement"
            else:
                return "metric-poor"

        else:
            return "metric-neutral"

    except:
        return "metric-neutral"

if __name__ == "__main__":
    generate_html_report()
