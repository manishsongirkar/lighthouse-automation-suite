#!/usr/bin/env python3
"""
Enhanced HTML Report Generator for Lighthouse Results
Generates a comprehensive color-coded HTML dashboard with optimization insights
"""
import csv
import pandas as pd
from datetime import datetime
import os

def load_additional_data():
    """Load additional insight data from CSV files"""
    opportunities = []
    accessibility_issues = []
    seo_details = []

    # Load opportunities
    if os.path.exists("lighthouse_opportunities.csv"):
        with open("lighthouse_opportunities.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            opportunities = list(reader)

    # Load accessibility issues
    if os.path.exists("lighthouse_accessibility.csv"):
        with open("lighthouse_accessibility.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            accessibility_issues = list(reader)

    # Load SEO details
    if os.path.exists("lighthouse_seo_details.csv"):
        with open("lighthouse_seo_details.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            seo_details = list(reader)

    return opportunities, accessibility_issues, seo_details


def generate_opportunities_section(opportunities):
    """Generate HTML for performance opportunities"""
    if not opportunities:
        return "<p>No optimization opportunities data available.</p>"

    # Group by URL and prioritize by potential savings
    url_opportunities = {}
    for opp in opportunities:
        url = opp['url']
        if url not in url_opportunities:
            url_opportunities[url] = []
        url_opportunities[url].append(opp)

    html = """
    <div class="insights-section">
        <h2>🚀 Performance Optimization Opportunities</h2>
        <p class="section-description">Recommendations to improve loading performance, ranked by potential impact.</p>
    """

    for url, opps in url_opportunities.items():
        # Sort by potential savings
        opps.sort(key=lambda x: float(x.get('potential_savings_ms', 0)), reverse=True)

        html += f"""
        <div class="url-insights">
            <h3 class="url-title">📊 {url}</h3>
            <div class="opportunities-grid">
        """

        for opp in opps[:5]:  # Show top 5 opportunities
            impact_class = f"impact-{opp['impact'].lower()}"
            savings = opp.get('potential_savings_s', '0')
            html += f"""
                <div class="opportunity-card {impact_class}">
                    <div class="opportunity-header">
                        <span class="impact-badge">{opp['impact']} Impact</span>
                        <span class="savings-badge">Save {savings}s</span>
                    </div>
                    <h4>{opp['title']}</h4>
                    <p class="opportunity-desc">{opp['description'][:100]}...</p>
                    <div class="device-tags">
                        <span class="device-tag {opp['device_type']}">{opp['device_type'].title()}</span>
                    </div>
                </div>
            """

        html += """
            </div>
        </div>
        """

    html += "</div>"
    return html


def generate_accessibility_section(accessibility_issues):
    """Generate HTML for accessibility issues"""
    if not accessibility_issues:
        return "<p>No accessibility issues data available.</p>"

    # Group by URL and severity
    url_issues = {}
    for issue in accessibility_issues:
        url = issue['url']
        if url not in url_issues:
            url_issues[url] = {'Critical': [], 'Warning': []}
        severity = issue.get('severity', 'Warning')
        url_issues[url][severity].append(issue)

    html = """
    <div class="insights-section">
        <h2>♿ Accessibility Issues & Recommendations</h2>
        <p class="section-description">Accessibility compliance issues that should be addressed for better user experience.</p>
    """

    for url, issues in url_issues.items():
        total_issues = len(issues['Critical']) + len(issues['Warning'])
        if total_issues == 0:
            continue

        html += f"""
        <div class="url-insights">
            <h3 class="url-title">♿ {url}</h3>
            <div class="accessibility-summary">
                <span class="issue-count critical">{len(issues['Critical'])} Critical</span>
                <span class="issue-count warning">{len(issues['Warning'])} Warnings</span>
            </div>
            <div class="accessibility-grid">
        """

        # Show critical issues first
        all_issues = issues['Critical'] + issues['Warning']
        for issue in all_issues[:6]:  # Show top 6 issues
            severity_class = f"severity-{issue['severity'].lower()}"
            html += f"""
                <div class="accessibility-card {severity_class}">
                    <div class="issue-header">
                        <span class="severity-badge">{issue['severity']}</span>
                        <span class="device-tag {issue['device_type']}">{issue['device_type'].title()}</span>
                    </div>
                    <h4>{issue['title']}</h4>
                    <p class="issue-desc">{issue['description'][:120]}...</p>
                </div>
            """

        html += """
            </div>
        </div>
        """

    html += "</div>"
    return html


def generate_enhanced_html_report(csv_file="pagespeed_results.csv", html_file="pagespeed_report.html"):
    """Generate an enhanced HTML dashboard report with insights"""
    try:
        df = pd.read_csv(csv_file)

        # Load additional data
        opportunities, accessibility_issues, seo_details = load_additional_data()

        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['url'], keep='first')
        final_count = len(df)

        if initial_count != final_count:
            print(f"⚠️  Warning: Removed {initial_count - final_count} duplicate URLs from data")

        print(f"📊 Processing {len(df)} unique URLs for enhanced HTML report")
        print(f"🚀 Found {len(opportunities)} optimization opportunities")
        print(f"♿ Found {len(accessibility_issues)} accessibility insights")
        print(f"🔍 Found {len(seo_details)} SEO details")

        # Enhanced CSS with new styles
        enhanced_css = """
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; line-height: 1.6; }
            .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { color: #1a73e8; margin: 0; font-size: 2.5em; }
            .header .subtitle { color: #666; margin-top: 10px; }

            /* Summary Cards */
            .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .summary-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
            .summary-card h3 { margin: 0 0 10px 0; }
            .summary-card .number { font-size: 2em; font-weight: bold; }

            /* Navigation Tabs */
            .nav-tabs { display: flex; background: #f8f9fa; border-radius: 8px; margin-bottom: 30px; padding: 5px; }
            .nav-tab { flex: 1; padding: 12px; text-align: center; background: none; border: none; cursor: pointer; border-radius: 6px; font-weight: 500; color: #333; transition: all 0.2s ease; }
            .nav-tab.active { background: #1a73e8; color: white; }
            .nav-tab:hover:not(.active) { background: #e3f2fd; color: #1a73e8; }
            .nav-tab.active:hover { background: #1565c0; color: white; }

            /* Insights Sections */
            .insights-section { margin-bottom: 40px; padding: 25px; background: #fafafa; border-radius: 8px; border-left: 4px solid #1a73e8; }
            .insights-section h2 { margin-top: 0; color: #1a73e8; }
            .section-description { color: #666; margin-bottom: 20px; font-style: italic; }

            /* URL Insights */
            .url-insights { margin-bottom: 30px; }
            .url-title { color: #333; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 20px; }

            /* Opportunity Cards */
            .opportunities-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); max-width: 100%; gap: 15px; }
            /* Limit to max 4 columns per row */
            @media (min-width: 1400px) {
                .opportunities-grid { grid-template-columns: repeat(4, 1fr); }
            }
            .opportunity-card { background: white; border-radius: 8px; padding: 20px; border-left: 4px solid; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .opportunity-card.impact-high { border-left-color: #f44336; }
            .opportunity-card.impact-medium { border-left-color: #ff9800; }
            .opportunity-card.impact-low { border-left-color: #4caf50; }

            .opportunity-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
            .impact-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; color: white; }
            .impact-badge { background: #1a73e8; }
            .savings-badge { padding: 4px 8px; border-radius: 4px; background: #0f9d58; color: white; font-size: 0.8em; font-weight: bold; }

            .opportunity-desc { color: #666; font-size: 0.9em; margin: 10px 0; }
            .device-tags { margin-top: 10px; }
            .device-tag { padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 5px; }
            .device-tag.mobile { background: #e3f2fd; color: #1976d2; }
            .device-tag.desktop { background: #f3e5f5; color: #7b1fa2; }

            /* Accessibility Cards */
            .accessibility-summary { margin-bottom: 15px; }
            .issue-count { padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; margin-right: 10px; }
            .issue-count.critical { background: #f44336; }
            .issue-count.warning { background: #ff9800; }

            .accessibility-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
            /* Limit to max 4 columns per row */
            @media (min-width: 1400px) {
                .accessibility-grid { grid-template-columns: repeat(4, 1fr); }
            }
            .accessibility-card { background: white; border-radius: 8px; padding: 15px; border-left: 4px solid; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .accessibility-card.severity-critical { border-left-color: #f44336; }
            .accessibility-card.severity-warning { border-left-color: #ff9800; }

            .issue-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
            .severity-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; color: white; }
            .severity-badge { background: #666; }
            .issue-desc { color: #666; font-size: 0.85em; }

            /* Existing table styles */
            .results-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            .results-table th, .results-table td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            .results-table th { background-color: #f8f9fa; font-weight: 600; }
            .score { padding: 4px 8px; border-radius: 4px; font-weight: bold; color: white; text-align: center; }
            .score-good { background: #0f9d58; }
            .score-average { background: #ff9800; }
            .score-poor { background: #f44336; }
            .url-cell { max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

            /* Content sections for tabs */
            .tab-content { display: none; }
            .tab-content.active { display: block; }

            /* Core Web Vitals Metrics */
            .vitals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-top: 20px; }
            .vitals-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #1a73e8; }
            .vitals-card h4 { margin: 0 0 15px 0; color: #333; font-size: 1.1em; }
            .metric-item { display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px; background: #f5f5f5; border-radius: 4px; }
            .metric-name { font-weight: 500; }
            .metric-value { font-family: monospace; font-weight: bold; padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.9em; }
            .metric-good { background: #0f9d58; }
            .metric-needs-improvement { background: #ff9800; }
            .metric-poor { background: #f44336; }
            .metric-neutral { background: #666; color: white; }

            /* Responsive */
            @media (max-width: 1399px) {
                .opportunities-grid { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
                .accessibility-grid { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
            }
            @media (max-width: 768px) {
                .opportunities-grid, .accessibility-grid { grid-template-columns: 1fr; }
                .summary { grid-template-columns: 1fr; }
                .nav-tabs { flex-direction: column; }
            }
        </style>

        <script>
            function showTab(tabName) {
                // Hide all tab contents
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(content => content.classList.remove('active'));

                // Remove active class from all tabs
                const tabs = document.querySelectorAll('.nav-tab');
                tabs.forEach(tab => tab.classList.remove('active'));

                // Show selected tab content
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }
        </script>
        """

        # Calculate summary statistics
        mobile_avg = df['mobile_performance'].dropna().mean() if 'mobile_performance' in df.columns else 0
        desktop_avg = df['desktop_performance'].dropna().mean() if 'desktop_performance' in df.columns else 0
        total_opportunities = len([o for o in opportunities if o.get('impact') == 'High'])
        critical_accessibility = len([a for a in accessibility_issues if a.get('severity') == 'Critical'])

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lighthouse Automation Suite - Enhanced Report</title>
    {enhanced_css}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Lighthouse Automation Suite</h1>
            <p class="subtitle">Enhanced Performance Analysis Report - Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <h3>📊 URLs Analyzed</h3>
                <div class="number">{len(df)}</div>
            </div>
            <div class="summary-card">
                <h3>📱 Mobile Avg Score</h3>
                <div class="number">{mobile_avg:.0f}</div>
            </div>
            <div class="summary-card">
                <h3>🖥️ Desktop Avg Score</h3>
                <div class="number">{desktop_avg:.0f}</div>
            </div>
            <div class="summary-card">
                <h3>🚀 High Impact Opportunities</h3>
                <div class="number">{total_opportunities}</div>
            </div>
            <div class="summary-card">
                <h3>⚠️ Critical A11y Issues</h3>
                <div class="number">{critical_accessibility}</div>
            </div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab('overview')">📊 Performance Overview</button>
            <button class="nav-tab" onclick="showTab('opportunities')">🚀 Optimization Opportunities</button>
            <button class="nav-tab" onclick="showTab('accessibility')">♿ Accessibility Issues</button>
        </div>

        <div id="overview" class="tab-content active">
        """

        # Add the existing performance tables (mobile and desktop)
        html_content += generate_performance_tables(df)

        html_content += """
        </div>

        <div id="opportunities" class="tab-content">
        """

        html_content += generate_opportunities_section(opportunities)

        html_content += """
        </div>

        <div id="accessibility" class="tab-content">
        """

        html_content += generate_accessibility_section(accessibility_issues)

        html_content += """
        </div>

    </div>
</body>
</html>
        """

        # Write the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Enhanced HTML report generated: {html_file}")
        print(f"   Open in browser: file://{os.path.abspath(html_file)}")

    except Exception as e:
        print(f"❌ Error generating enhanced HTML report: {e}")


def generate_performance_tables(df):
    """Generate the existing performance tables with Core Web Vitals matrix"""
    def get_score_class(score):
        if pd.isna(score):
            return 'score-poor'
        if score >= 90:
            return 'score-good'
        elif score >= 50:
            return 'score-average'
        else:
            return 'score-poor'

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

    html = """
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

        html += f"""
                <tr>
                    <td class="url-cell" title="{row['url']}">{row['url']}</td>
                    <td><span class="score {get_score_class(row.get('mobile_performance'))}">{row.get('mobile_performance', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('mobile_accessibility'))}">{row.get('mobile_accessibility', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('mobile_best_practices'))}">{row.get('mobile_best_practices', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('mobile_seo'))}">{row.get('mobile_seo', 'N/A')}</span></td>
                    <td>{pagespeed_link}</td>
                </tr>
        """

    html += """
            </tbody>
        </table>

        <h2 style="margin-top: 40px;">🖥️ Desktop Performance Scores</h2>
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

        html += f"""
                <tr>
                    <td class="url-cell" title="{row['url']}">{row['url']}</td>
                    <td><span class="score {get_score_class(row.get('desktop_performance'))}">{row.get('desktop_performance', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('desktop_accessibility'))}">{row.get('desktop_accessibility', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('desktop_best_practices'))}">{row.get('desktop_best_practices', 'N/A')}</span></td>
                    <td><span class="score {get_score_class(row.get('desktop_seo'))}">{row.get('desktop_seo', 'N/A')}</span></td>
                    <td>{pagespeed_link}</td>
                </tr>
        """

    html += """
            </tbody>
        </table>

        <h2 style="margin-top: 40px;">⚡ Core Web Vitals & Performance Metrics</h2>
        <p style="color: #666; margin-bottom: 15px;">Detailed performance metrics for each analyzed URL with color-coded indicators</p>

        <div class="vitals-grid">
    """

    # Add Core Web Vitals for each URL
    for _, row in df.iterrows():
        # Core Web Vitals mapping
        mobile_metrics = {}
        desktop_metrics = {}

        # Mobile metrics
        if pd.notna(row.get('mobile_first_contentful_paint')):
            mobile_metrics['First Contentful Paint'] = row['mobile_first_contentful_paint']
        if pd.notna(row.get('mobile_largest_contentful_paint')):
            mobile_metrics['Largest Contentful Paint'] = row['mobile_largest_contentful_paint']
        if pd.notna(row.get('mobile_total_blocking_time')):
            mobile_metrics['Total Blocking Time'] = row['mobile_total_blocking_time']
        if pd.notna(row.get('mobile_cumulative_layout_shift')):
            mobile_metrics['Cumulative Layout Shift'] = row['mobile_cumulative_layout_shift']
        if pd.notna(row.get('mobile_speed_index')):
            mobile_metrics['Speed Index'] = row['mobile_speed_index']

        # Desktop metrics
        if pd.notna(row.get('desktop_first_contentful_paint')):
            desktop_metrics['First Contentful Paint'] = row['desktop_first_contentful_paint']
        if pd.notna(row.get('desktop_largest_contentful_paint')):
            desktop_metrics['Largest Contentful Paint'] = row['desktop_largest_contentful_paint']
        if pd.notna(row.get('desktop_total_blocking_time')):
            desktop_metrics['Total Blocking Time'] = row['desktop_total_blocking_time']
        if pd.notna(row.get('desktop_cumulative_layout_shift')):
            desktop_metrics['Cumulative Layout Shift'] = row['desktop_cumulative_layout_shift']
        if pd.notna(row.get('desktop_speed_index')):
            desktop_metrics['Speed Index'] = row['desktop_speed_index']

        pagespeed_url = row.get('final_url', '')
        pagespeed_link = f'<a href="{pagespeed_url}" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: 500; font-size: 0.9em;">📊 View Full Report</a>' if pagespeed_url else ''

        html += f"""
            <div class="vitals-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="margin: 0;">🌐 {row['url']}</h4>
                    {pagespeed_link}
                </div>

                <div style="margin-bottom: 20px;">
                    <strong>📱 Mobile Metrics:</strong>
        """

        if mobile_metrics:
            for metric_name, value in mobile_metrics.items():
                # Get the original column name for threshold checking
                col_name = f"mobile_{metric_name.lower().replace(' ', '_')}"
                metric_class = get_metric_class(col_name, value)
                html += f"""
                    <div class="metric-item">
                        <span class="metric-name">{metric_name}</span>
                        <span class="metric-value {metric_class}">{value}</span>
                    </div>
                """
        else:
            html += '<p style="color: #666; font-style: italic; margin: 10px 0;">No mobile metrics available</p>'

        html += """
                </div>

                <div>
                    <strong>🖥️ Desktop Metrics:</strong>
        """

        if desktop_metrics:
            for metric_name, value in desktop_metrics.items():
                # Get the original column name for threshold checking
                col_name = f"desktop_{metric_name.lower().replace(' ', '_')}"
                metric_class = get_metric_class(col_name, value)
                html += f"""
                    <div class="metric-item">
                        <span class="metric-name">{metric_name}</span>
                        <span class="metric-value {metric_class}">{value}</span>
                    </div>
                """
        else:
            html += '<p style="color: #666; font-style: italic; margin: 10px 0;">No desktop metrics available</p>'

        html += """
                </div>
            </div>
        """

    html += """
        </div>

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
    """

    return html


if __name__ == "__main__":
    generate_enhanced_html_report()
