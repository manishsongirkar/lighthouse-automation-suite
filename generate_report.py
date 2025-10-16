#!/usr/bin/env python3
"""
PageSpeed Results Report Generator
Reads pagespeed_results.csv and generates formatted reports
"""
import csv
import pandas as pd
from datetime import datetime

def generate_summary_report(csv_file="pagespeed_results.csv"):
    """Generate a summary report from PageSpeed results"""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        print("=" * 80)
        print("📊 PAGESPEED INSIGHTS ANALYSIS REPORT")
        print("=" * 80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total URLs Analyzed: {len(df)}")
        print("-" * 80)

        # Performance Score Analysis
        print("\n📱 MOBILE PERFORMANCE SCORES")
        print("-" * 40)
        for _, row in df.iterrows():
            url = row['url']
            perf = row['mobile_performance']
            acc = row['mobile_accessibility']
            bp = row['mobile_best_practices']
            seo = row['mobile_seo']
            print(f"{url:<35} | Perf: {perf:>3} | Acc: {acc:>3} | BP: {bp:>3} | SEO: {seo:>3}")

        print(f"\nMobile Average Scores:")
        print(f"  Performance:     {df['mobile_performance'].mean():.1f}")
        print(f"  Accessibility:   {df['mobile_accessibility'].mean():.1f}")
        print(f"  Best Practices:  {df['mobile_best_practices'].mean():.1f}")
        print(f"  SEO:            {df['mobile_seo'].mean():.1f}")

        print("\n🖥️  DESKTOP PERFORMANCE SCORES")
        print("-" * 40)
        for _, row in df.iterrows():
            url = row['url']
            perf = row['desktop_performance']
            acc = row['desktop_accessibility']
            bp = row['desktop_best_practices']
            seo = row['desktop_seo']
            print(f"{url:<35} | Perf: {perf:>3} | Acc: {acc:>3} | BP: {bp:>3} | SEO: {seo:>3}")

        print(f"\nDesktop Average Scores:")
        print(f"  Performance:     {df['desktop_performance'].mean():.1f}")
        print(f"  Accessibility:   {df['desktop_accessibility'].mean():.1f}")
        print(f"  Best Practices:  {df['desktop_best_practices'].mean():.1f}")
        print(f"  SEO:            {df['desktop_seo'].mean():.1f}")

        # Performance Issues (scores below 90)
        print("\n⚠️  PERFORMANCE ISSUES (Scores < 90)")
        print("-" * 50)
        issues_found = False

        for _, row in df.iterrows():
            url = row['url']
            issues = []

            if row['mobile_performance'] < 90:
                issues.append(f"Mobile Performance: {row['mobile_performance']}")
            if row['desktop_performance'] < 90:
                issues.append(f"Desktop Performance: {row['desktop_performance']}")
            if row['mobile_accessibility'] < 90:
                issues.append(f"Mobile Accessibility: {row['mobile_accessibility']}")
            if row['desktop_accessibility'] < 90:
                issues.append(f"Desktop Accessibility: {row['desktop_accessibility']}")

            if issues:
                print(f"\n{url}:")
                for issue in issues:
                    print(f"  ❌ {issue}")
                issues_found = True

        if not issues_found:
            print("✅ No critical issues found!")

        # Core Web Vitals Summary
        print("\n⚡ CORE WEB VITALS SUMMARY")
        print("-" * 50)

        vitals_metrics = [
            ('mobile_first_contentful_paint', 'Mobile First Contentful Paint'),
            ('mobile_largest_contentful_paint', 'Mobile Largest Contentful Paint'),
            ('mobile_total_blocking_time', 'Mobile Total Blocking Time'),
            ('mobile_cumulative_layout_shift', 'Mobile Cumulative Layout Shift'),
            ('mobile_speed_index', 'Mobile Speed Index'),
            ('desktop_first_contentful_paint', 'Desktop First Contentful Paint'),
            ('desktop_largest_contentful_paint', 'Desktop Largest Contentful Paint'),
            ('desktop_total_blocking_time', 'Desktop Total Blocking Time'),
            ('desktop_cumulative_layout_shift', 'Desktop Cumulative Layout Shift'),
            ('desktop_speed_index', 'Desktop Speed Index')
        ]

        available_metrics = []
        for col_name, display_name in vitals_metrics:
            if col_name in df.columns and not df[col_name].isna().all():
                available_metrics.append((col_name, display_name))

        if available_metrics:
            print("Average Core Web Vitals across all URLs:")
            print()

            # Group by mobile/desktop
            mobile_metrics = [(col, name) for col, name in available_metrics if col.startswith('mobile_')]
            desktop_metrics = [(col, name) for col, name in available_metrics if col.startswith('desktop_')]

            if mobile_metrics:
                print("📱 MOBILE METRICS:")
                for col_name, display_name in mobile_metrics:
                    # Handle different data types and formats
                    values = []
                    for val in df[col_name].dropna():
                        try:
                            # Remove 's', 'ms', commas and convert to float
                            clean_val = str(val).replace('s', '').replace('ms', '').replace(',', '').strip()
                            if clean_val and clean_val.replace('.', '').replace('-', '').isdigit():
                                values.append(float(clean_val))
                        except:
                            continue

                    if values:
                        avg_val = sum(values) / len(values)
                        metric_short = display_name.replace('Mobile ', '')
                        if 'Layout Shift' in display_name:
                            print(f"  {metric_short:<25}: {avg_val:.3f}")
                        elif any(unit in col_name for unit in ['paint', 'blocking', 'index']):
                            if avg_val >= 1:
                                print(f"  {metric_short:<25}: {avg_val:.1f}s")
                            else:
                                print(f"  {metric_short:<25}: {avg_val*1000:.0f}ms")
                        else:
                            print(f"  {metric_short:<25}: {avg_val:.1f}")
                print()

            if desktop_metrics:
                print("🖥️  DESKTOP METRICS:")
                for col_name, display_name in desktop_metrics:
                    values = []
                    for val in df[col_name].dropna():
                        try:
                            clean_val = str(val).replace('s', '').replace('ms', '').replace(',', '').strip()
                            if clean_val and clean_val.replace('.', '').replace('-', '').isdigit():
                                values.append(float(clean_val))
                        except:
                            continue

                    if values:
                        avg_val = sum(values) / len(values)
                        metric_short = display_name.replace('Desktop ', '')
                        if 'Layout Shift' in display_name:
                            print(f"  {metric_short:<25}: {avg_val:.3f}")
                        elif any(unit in col_name for unit in ['paint', 'blocking', 'index']):
                            if avg_val >= 1:
                                print(f"  {metric_short:<25}: {avg_val:.1f}s")
                            else:
                                print(f"  {metric_short:<25}: {avg_val*1000:.0f}ms")
                        else:
                            print(f"  {metric_short:<25}: {avg_val:.1f}")
        else:
            print("No Core Web Vitals data found in results.")

        print("\n" + "=" * 80)
        print("Report complete! CSV file available at: pagespeed_results.csv")

    except FileNotFoundError:
        print(f"❌ Error: {csv_file} not found. Run main.py first to generate results.")
    except Exception as e:
        print(f"❌ Error generating report: {e}")

def export_to_excel(csv_file="pagespeed_results.csv", excel_file="pagespeed_report.xlsx"):
    """Export results to Excel with formatting"""
    try:
        df = pd.read_csv(csv_file)

        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='PageSpeed Results', index=False)

            # Summary sheet
            summary_data = {
                'Metric': ['Mobile Performance', 'Mobile Accessibility', 'Mobile Best Practices', 'Mobile SEO',
                          'Desktop Performance', 'Desktop Accessibility', 'Desktop Best Practices', 'Desktop SEO'],
                'Average Score': [
                    df['mobile_performance'].mean(),
                    df['mobile_accessibility'].mean(),
                    df['mobile_best_practices'].mean(),
                    df['mobile_seo'].mean(),
                    df['desktop_performance'].mean(),
                    df['desktop_accessibility'].mean(),
                    df['desktop_best_practices'].mean(),
                    df['desktop_seo'].mean()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        print(f"✅ Excel report exported to: {excel_file}")

    except ImportError:
        print("❌ openpyxl not installed. Install with: pip install openpyxl")
    except Exception as e:
        print(f"❌ Error exporting to Excel: {e}")

if __name__ == "__main__":
    # Generate summary report
    generate_summary_report()

    # Optionally export to Excel (uncomment if you have openpyxl installed)
    # export_to_excel()
