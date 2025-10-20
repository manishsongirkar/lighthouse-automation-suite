#!/usr/bin/env python3
"""
Enhanced HTML Report Generator for Lighthouse Results
Generates a comprehensive color-coded HTML dashboard
"""
import pandas as pd
from datetime import datetime
import os

def generate_html_report(csv_file="pagespeed_results.csv", html_file="pagespeed_report.html"):
    """Generate an HTML dashboard report"""
    try:
        df = pd.read_csv(csv_file)

        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['url'], keep='first')
        final_count = len(df)

        if initial_count != final_count:
            print(f"⚠️  Warning: Removed {initial_count - final_count} duplicate URLs from data")

        print(f"📊 Processing {len(df)} unique URLs for enhanced HTML report")

        # PageSpeed Insights inspired CSS matching pagespeed.web.dev design
        enhanced_css = """
        <style>
            /* Google PageSpeed Insights Design System */
            :root {
                --psi-blue: #4285f4;
                --psi-green: #0cce6b;
                --psi-orange: #ffa400;
                --psi-red: #ff5722;
                --psi-gray-50: #f8f9fa;
                --psi-gray-100: #f1f3f4;
                --psi-gray-200: #e8eaed;
                --psi-gray-600: #5f6368;
                --psi-gray-700: #3c4043;
                --psi-gray-900: #202124;
                --psi-shadow: 0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
                --psi-border-radius: 8px;
            }

            body {
                font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                margin: 0;
                padding: 24px;
                background: var(--psi-gray-50);
                color: var(--psi-gray-900);
                line-height: 1.5;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: var(--psi-border-radius);
                box-shadow: var(--psi-shadow);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, var(--psi-blue) 0%, #1a73e8 100%);
                color: white;
                text-align: center;
                padding: 32px 24px;
            }

            .header h1 {
                margin: 0;
                font-size: 32px;
                font-weight: 400;
                font-family: 'Google Sans', sans-serif;
            }

            .header .subtitle {
                margin-top: 8px;
                opacity: 0.9;
                font-size: 16px;
                font-weight: 300;
            }

            /* Summary Cards - Material Design Cards */
            .summary {
                display: flex;
                gap: 16px;
                margin: 24px;
                flex-wrap: wrap;
            }

            .summary-card {
                flex: 1;
                background: white;
                border: 1px solid var(--psi-gray-200);
                border-radius: var(--psi-border-radius);
                padding: 24px;
                text-align: center;
                min-width: 180px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                transition: box-shadow 0.2s ease;
            }

            .summary-card:hover {
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            }

            .summary-card h3 {
                margin: 0 0 12px 0;
                font-size: 14px;
                color: var(--psi-gray-600);
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .summary-card .number {
                font-size: 40px;
                font-weight: 300;
                margin: 0;
                color: var(--psi-blue);
                font-family: 'Google Sans', sans-serif;
            }

            /* Content sections */
            .content-section {
                margin: 0 24px 32px 24px;
            }

            .content-section h2 {
                color: var(--psi-gray-900);
                border-bottom: 1px solid var(--psi-gray-200);
                padding-bottom: 12px;
                margin-bottom: 24px;
                font-size: 24px;
                font-weight: 400;
                font-family: 'Google Sans', sans-serif;
            }

            /* Section headers */
            .section-header {
                color: var(--psi-gray-700);
                border-left: 4px solid var(--psi-blue);
                padding-left: 16px;
                margin: 32px 0 20px 0;
                font-size: 20px;
                font-weight: 400;
                font-family: 'Google Sans', sans-serif;
            }

            .mobile-header {
                border-left-color: var(--psi-blue);
            }

            .desktop-header {
                border-left-color: var(--psi-green);
            }

            /* Table styles - Material Design inspired */
            .results-table {
                width: 100%;
                border-collapse: collapse;
                margin: 16px 0;
                background: white;
                border-radius: var(--psi-border-radius);
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }

            .results-table th {
                background: var(--psi-gray-50);
                padding: 16px 12px;
                text-align: left;
                border-bottom: 1px solid var(--psi-gray-200);
                font-weight: 500;
                color: var(--psi-gray-700);
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.25px;
            }

            .results-table td {
                padding: 16px 12px;
                border-bottom: 1px solid var(--psi-gray-100);
                font-size: 14px;
            }

            .results-table tbody tr:hover {
                background-color: rgba(66, 133, 244, 0.04);
            }

            .results-table tbody tr:last-child td {
                border-bottom: none;
            }

            /* Circular Progress Indicators - PageSpeed Style */
            .circle-progress {
                position: relative;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 48px;
                height: 48px;
                margin: 0 auto;
            }

            .circle-progress svg {
                transform: rotate(-90deg);
                width: 48px;
                height: 48px;
            }

            .circle-progress .circle-bg {
                fill: none;
                stroke: var(--psi-gray-200);
                stroke-width: 4;
            }

            .circle-progress .circle-progress-bar {
                fill: none;
                stroke-width: 4;
                stroke-linecap: round;
                transition: stroke-dasharray 1.2s cubic-bezier(0.4, 0, 0.2, 1);
                stroke-dasharray: 0 125.6; /* Initial state - empty circle */
                /* Animation will be added dynamically via JavaScript */
            }

            @keyframes circleReveal {
                0% {
                    stroke-dasharray: 0 125.6;
                    opacity: 0.6;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    stroke-dasharray: var(--target-progress, 0) var(--target-remaining, 125.6);
                    opacity: 1;
                }
            }

            /* Smooth fade-in animation for the entire circle */
            .circle-progress {
                /* Animation will be added dynamically via JavaScript */
                opacity: 0;
                transform: scale(0.8);
            }

            /* Active state when animation should start */
            .circle-progress.animate {
                animation: fadeInScale 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
                animation-delay: var(--animation-delay, 0s);
            }

            .circle-progress.animate .circle-progress-bar {
                animation: circleReveal 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
                animation-delay: var(--animation-delay, 0s);
            }

            .circle-progress.animate .circle-text {
                animation: textCountUp 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
                animation-delay: calc(var(--animation-delay, 0s) + 0.3s);
            }

            @keyframes fadeInScale {
                0% {
                    opacity: 0;
                    transform: scale(0.8);
                }
                100% {
                    opacity: 1;
                    transform: scale(1);
                }
            }

            /* Text animation */
            .circle-progress .circle-text {
                opacity: 0;
            }

            @keyframes textCountUp {
                0% {
                    opacity: 0;
                    transform: translate(-50%, -50%) scale(0.5);
                }
                100% {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
            }

            .circle-progress .circle-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 12px;
                font-weight: 500;
                font-family: 'Google Sans', sans-serif;
            }

            .circle-progress.good .circle-progress-bar { stroke: var(--psi-green); }
            .circle-progress.good .circle-text { color: var(--psi-green); }

            .circle-progress.average .circle-progress-bar { stroke: var(--psi-orange); }
            .circle-progress.average .circle-text { color: var(--psi-orange); }

            .circle-progress.poor .circle-progress-bar { stroke: var(--psi-red); }
            .circle-progress.poor .circle-text { color: var(--psi-red); }

            .circle-progress.na .circle-progress-bar { stroke: var(--psi-gray-200); }
            .circle-progress.na .circle-text { color: var(--psi-gray-600); }

            /* Score badges - PageSpeed style (fallback for Core Web Vitals) */
            .score {
                padding: 4px 12px;
                border-radius: 16px;
                font-weight: 500;
                color: white;
                text-align: center;
                display: inline-block;
                min-width: 32px;
                font-size: 14px;
                font-family: 'Google Sans', sans-serif;
            }

            .score-good { background: var(--psi-green); }
            .score-average { background: var(--psi-orange); }
            .score-poor { background: var(--psi-red); }

            /* Performance tables with circles */
            .performance-cell {
                text-align: center;
                padding: 16px 8px;
            }

            /* Section animation improvements */
            [style*="margin-bottom: 64px"] {
                opacity: 1;
                transform: translateY(0);
                transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            }

            /* Smooth section entry animation */
            .section-animated {
                opacity: 1;
                transform: translateY(0);
            }

            .url-cell {
                max-width: 280px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                color: var(--psi-blue);
                font-weight: 400;
            }

            /* Core Web Vitals section header */
            .cwv-header {
                font-size: 16px;
                font-weight: 500;
                color: var(--psi-gray-700);
                margin: 24px 0 16px 0;
                padding: 12px 16px;
                background: var(--psi-gray-50);
                border-radius: var(--psi-border-radius);
                border-left: 4px solid var(--psi-orange);
            }

            /* Legend - PageSpeed style */
            .legend {
                margin-top: 32px;
                padding: 24px;
                background: var(--psi-gray-50);
                border-radius: var(--psi-border-radius);
                border: 1px solid var(--psi-gray-200);
            }

            .legend-title {
                font-size: 16px;
                font-weight: 500;
                color: var(--psi-gray-900);
                margin: 0 0 16px 0;
                font-family: 'Google Sans', sans-serif;
            }

            .legend-item {
                margin: 8px 16px 8px 0;
                display: inline-block;
            }

            .thresholds {
                margin-top: 20px;
                font-size: 13px;
                color: var(--psi-gray-600);
                line-height: 1.6;
            }

            .thresholds h4 {
                font-size: 14px;
                font-weight: 500;
                color: var(--psi-gray-700);
                margin: 16px 0 12px 0;
                font-family: 'Google Sans', sans-serif;
            }

            .threshold-item {
                margin: 8px 0;
                padding-left: 16px;
                position: relative;
            }

            .threshold-item:before {
                content: "•";
                color: var(--psi-blue);
                position: absolute;
                left: 0;
                font-weight: bold;
            }

            /* URL Header with View Report Button */
            .url-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 24px;
                flex-wrap: wrap;
                gap: 16px;
            }

            .url-title {
                color: var(--psi-blue);
                font-size: 20px;
                margin: 0;
                font-family: 'Google Sans', sans-serif;
                flex: 1;
            }

            .view-report-btn {
                background: var(--psi-blue);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Google Sans', sans-serif;
                transition: background-color 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            .view-report-btn:hover {
                background: #3367d6;
                text-decoration: none;
                color: white;
            }

            .view-report-btn:visited {
                color: white;
            }

            /* Responsive Design */
            @media (max-width: 768px) {
                body { padding: 16px; }
                .summary { flex-direction: column; margin: 16px; }
                .content-section { margin: 0 16px 24px 16px; }
                .results-table { font-size: 13px; }
                .results-table th, .results-table td { padding: 12px 8px; }
                .url-cell { max-width: 150px; }
                .header { padding: 24px 16px; }
                .header h1 { font-size: 28px; }
                .url-header { flex-direction: column; align-items: flex-start; }
                .url-title { font-size: 18px; }
            }

            /* Google Fonts import */
            @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500&family=Roboto:wght@300;400;500&display=swap');
        </style>

        <script>
            function createCircularProgress(score, size = 48) {
                // Handle non-numeric or missing scores
                if (!score || isNaN(score) || score === 'N/A') {
                    return `
                        <div class="circle-progress na">
                            <svg>
                                <circle class="circle-bg" cx="24" cy="24" r="20"></circle>
                                <circle class="circle-progress-bar" cx="24" cy="24" r="20"></circle>
                            </svg>
                            <div class="circle-text">—</div>
                        </div>
                    `;
                }

                const numScore = parseInt(score);
                const circumference = 2 * Math.PI * 20; // radius = 20
                const strokeDasharray = (numScore / 100) * circumference;
                const remainingDash = circumference - strokeDasharray;

                let progressClass = 'poor';
                if (numScore >= 90) {
                    progressClass = 'good';
                } else if (numScore >= 50) {
                    progressClass = 'average';
                }

                return `
                    <div class="circle-progress ${progressClass}">
                        <svg>
                            <circle class="circle-bg" cx="24" cy="24" r="20"></circle>
                            <circle class="circle-progress-bar" cx="24" cy="24" r="20"></circle>
                        </svg>
                        <div class="circle-text">${numScore}</div>
                    </div>
                `;
            }

            // Enhanced animation controller for individual circle sections
            function animateCirclesInSection(section, isInitial = false) {
                const circles = section.querySelectorAll('.circle-progress:not(.animated)');

                circles.forEach((circle, index) => {
                    const progressBar = circle.querySelector('.circle-progress-bar');
                    const textElement = circle.querySelector('.circle-text');

                    // Get the actual score from data attribute
                    const scoreFromData = circle.getAttribute('data-score');

                    // Skip non-numeric scores or N/A cases (but allow legitimate 0 scores)
                    if (!scoreFromData || scoreFromData === 'N/A' || isNaN(parseInt(scoreFromData))) {
                        circle.classList.add('animated');
                        // Still show the circle but without animation
                        circle.style.opacity = '1';
                        circle.style.transform = 'scale(1)';
                        return;
                    }

                    // Check if it's an N/A case by looking at the text content
                    const currentText = textElement.textContent;
                    if (currentText === '—' || currentText === 'N/A') {
                        circle.classList.add('animated');
                        // Still show the circle but without animation
                        circle.style.opacity = '1';
                        circle.style.transform = 'scale(1)';
                        return;
                    }

                    const score = parseInt(scoreFromData);
                    const circumference = 2 * Math.PI * 20;
                    const strokeDasharray = (score / 100) * circumference;
                    const remainingDash = circumference - strokeDasharray;

                    // Set CSS custom properties for animation
                    circle.style.setProperty('--target-progress', strokeDasharray);
                    circle.style.setProperty('--target-remaining', remainingDash);
                    circle.style.setProperty('--animation-delay', `${index * 0.15}s`);

                    // Mark as animated to prevent duplicate animations
                    circle.classList.add('animated');

                    // Trigger CSS animations by adding the animate class
                    setTimeout(() => {
                        circle.classList.add('animate');

                        // Start number counting slightly after circle animation begins
                        setTimeout(() => {
                            animateCountUp(textElement, 0, score, 1000);
                        }, 200);
                    }, index * 150);
                });
            }

            // Smooth number counting animation
            function animateCountUp(element, start, end, duration) {
                const startTime = performance.now();

                function updateCount(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);

                    // Use easing function for smooth animation
                    const easeOutQuart = 1 - Math.pow(1 - progress, 4);
                    const currentValue = Math.floor(start + (end - start) * easeOutQuart);

                    element.textContent = currentValue;

                    if (progress < 1) {
                        requestAnimationFrame(updateCount);
                    } else {
                        element.textContent = end;
                    }
                }

                requestAnimationFrame(updateCount);
            }

            // Initialize animations when DOM loads
            document.addEventListener('DOMContentLoaded', function() {
                // Use Intersection Observer for performance-optimized animations
                if ('IntersectionObserver' in window) {
                    const observer = new IntersectionObserver((entries) => {
                        entries.forEach(entry => {
                            if (entry.isIntersecting && !entry.target.classList.contains('section-animated')) {
                                entry.target.classList.add('section-animated');
                                // Trigger animations for this section
                                setTimeout(() => {
                                    animateCirclesInSection(entry.target);
                                }, 100);
                            }
                        });
                    }, {
                        threshold: 0.3, // Trigger when 30% of the section is visible
                        rootMargin: '50px 0px -50px 0px' // Start animation slightly before coming into view
                    });

                    // Observe all URL sections
                    document.querySelectorAll('[style*="margin-bottom: 64px"]').forEach(section => {
                        observer.observe(section);
                    });

                    // Animate the first section immediately if it's visible
                    const firstSection = document.querySelector('[style*="margin-bottom: 64px"]');
                    if (firstSection) {
                        const rect = firstSection.getBoundingClientRect();
                        if (rect.top < window.innerHeight) {
                            setTimeout(() => {
                                firstSection.classList.add('section-animated');
                                animateCirclesInSection(firstSection, true);
                            }, 200);
                        }
                    }
                } else {
                    // Fallback for browsers without IntersectionObserver
                    setTimeout(() => {
                        const allSections = document.querySelectorAll('[style*="margin-bottom: 64px"]');
                        allSections.forEach((section, sectionIndex) => {
                            setTimeout(() => {
                                section.classList.add('section-animated');
                                animateCirclesInSection(section);
                            }, sectionIndex * 500);
                        });
                    }, 200);
                }
            });
        </script>
        """

        # Calculate summary statistics
        mobile_avg = df['mobile_performance'].dropna().mean() if 'mobile_performance' in df.columns else 0
        desktop_avg = df['desktop_performance'].dropna().mean() if 'desktop_performance' in df.columns else 0
        mobile_acc_avg = df['mobile_accessibility'].dropna().mean() if 'mobile_accessibility' in df.columns else 0
        desktop_acc_avg = df['desktop_accessibility'].dropna().mean() if 'desktop_accessibility' in df.columns else 0

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PageSpeed Insights - Performance Report</title>
    {enhanced_css}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>PageSpeed Insights</h1>
            <p class="subtitle">Performance Analysis Report • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <h3>URLs Analyzed</h3>
                <div class="number">{len(df)}</div>
            </div>
        </div>

        <div class="content-section">
            <h2>Performance Overview</h2>
        """

        # Add the existing performance tables (mobile and desktop)
        html_content += generate_performance_tables(df)

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
    """Generate URL-specific performance tables - one URL at a time with mobile/desktop and Core Web Vitals"""
    def get_score_class(score):
        if pd.isna(score):
            return 'score-poor'
        if score >= 90:
            return 'score-good'
        elif score >= 50:
            return 'score-average'
        else:
            return 'score-poor'

    def create_circular_progress(score):
        """Generate circular progress indicator HTML like PageSpeed Insights with smooth animations"""
        # Handle non-numeric or missing scores
        if pd.isna(score) or score == '' or score == 'N/A':
            return '''
                <div class="circle-progress na" data-score="0">
                    <svg>
                        <circle class="circle-bg" cx="24" cy="24" r="20"></circle>
                        <circle class="circle-progress-bar" cx="24" cy="24" r="20"></circle>
                    </svg>
                    <div class="circle-text">—</div>
                </div>
            '''

        try:
            num_score = int(float(score))
        except (ValueError, TypeError):
            return '''
                <div class="circle-progress na" data-score="0">
                    <svg>
                        <circle class="circle-bg" cx="24" cy="24" r="20"></circle>
                        <circle class="circle-progress-bar" cx="24" cy="24" r="20"></circle>
                    </svg>
                    <div class="circle-text">—</div>
                </div>
            '''

        # Ensure score is within valid range
        num_score = max(0, min(100, num_score))

        circumference = 2 * 3.14159 * 20  # radius = 20
        stroke_dasharray = (num_score / 100) * circumference
        remaining_dash = circumference - stroke_dasharray

        progress_class = 'poor'
        if num_score >= 90:
            progress_class = 'good'
        elif num_score >= 50:
            progress_class = 'average'

        return f'''
            <div class="circle-progress {progress_class}"
                 data-score="{num_score}"
                 style="--target-progress: {stroke_dasharray}; --target-remaining: {remaining_dash};">
                <svg>
                    <circle class="circle-bg" cx="24" cy="24" r="20"></circle>
                    <circle class="circle-progress-bar" cx="24" cy="24" r="20"></circle>
                </svg>
                <div class="circle-text">0</div>
            </div>
        '''

    def get_metric_class(metric_name, value_str):
        """Return CSS class based on Core Web Vitals thresholds"""
        try:
            # Handle different value formats
            if pd.isna(value_str) or value_str == '' or value_str == 'N/A':
                return 'score-poor'

            # Convert value to float, handling 's' and 'ms' suffixes
            value_clean = str(value_str).replace('s', '').replace('ms', '').replace(',', '').strip()
            if not value_clean:
                return 'score-poor'

            value = float(value_clean)

            # Convert ms to seconds for TBT
            if 'ms' in str(value_str):
                value = value / 1000

            # Core Web Vitals thresholds
            thresholds = {
                'mobile_first_contentful_paint': (1.8, 3.0),
                'desktop_first_contentful_paint': (1.8, 3.0),
                'mobile_largest_contentful_paint': (2.5, 4.0),
                'desktop_largest_contentful_paint': (2.5, 4.0),
                'mobile_total_blocking_time': (0.2, 0.6),  # in seconds
                'desktop_total_blocking_time': (0.2, 0.6),  # in seconds
                'mobile_cumulative_layout_shift': (0.1, 0.25),
                'desktop_cumulative_layout_shift': (0.1, 0.25),
                'mobile_speed_index': (3.4, 5.8),
                'desktop_speed_index': (3.4, 5.8)
            }

            if metric_name in thresholds:
                good_threshold, poor_threshold = thresholds[metric_name]
                if value <= good_threshold:
                    return 'score-good'
                elif value <= poor_threshold:
                    return 'score-average'
                else:
                    return 'score-poor'

            return 'score-poor'
        except (ValueError, TypeError):
            return 'score-poor'

    html = ""

    # Generate URL-specific sections
    for index, (_, row) in enumerate(df.iterrows(), 1):
        url = row.get('url', 'N/A')
        pagespeed_url = row.get('final_url', '')

        html += f"""
        <!-- URL {index} Performance Section -->
        <div style="margin-bottom: 64px; border-bottom: 1px solid var(--psi-gray-200); padding-bottom: 32px;">
            <div class="url-header">
                <h3 class="url-title">🌐 {url}</h3>
                {f'<a href="{pagespeed_url}" target="_blank" class="view-report-btn">📊 View Report</a>' if pagespeed_url else ''}
            </div>            <!-- Performance Scores -->
            <div style="display: flex; gap: 24px; margin-bottom: 32px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <h4 class="section-header mobile-header">📱 Mobile Performance</h4>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>Performance</th>
                                <th>Accessibility</th>
                                <th>Best Practices</th>
                                <th>SEO</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="performance-cell">{create_circular_progress(row.get('mobile_performance', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('mobile_accessibility', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('mobile_best_practices', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('mobile_seo', 'N/A'))}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div style="flex: 1; min-width: 300px;">
                    <h4 class="section-header desktop-header">🖥️ Desktop Performance</h4>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>Performance</th>
                                <th>Accessibility</th>
                                <th>Best Practices</th>
                                <th>SEO</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="performance-cell">{create_circular_progress(row.get('desktop_performance', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('desktop_accessibility', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('desktop_best_practices', 'N/A'))}</td>
                                <td class="performance-cell">{create_circular_progress(row.get('desktop_seo', 'N/A'))}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Core Web Vitals -->
            <div class="cwv-header">⚡ Core Web Vitals</div>
            <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <h5 style="color: var(--psi-gray-700); margin: 16px 0 12px 0; font-size: 14px; font-weight: 500;">� Mobile</h5>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>FCP</th>
                                <th>LCP</th>
                                <th>TBT</th>
                                <th>CLS</th>
                                <th>SI</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span class="score {get_metric_class('mobile_first_contentful_paint', row.get('mobile_first_contentful_paint', 'N/A'))}">{row.get('mobile_first_contentful_paint', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('mobile_largest_contentful_paint', row.get('mobile_largest_contentful_paint', 'N/A'))}">{row.get('mobile_largest_contentful_paint', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('mobile_total_blocking_time', row.get('mobile_total_blocking_time', 'N/A'))}">{row.get('mobile_total_blocking_time', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('mobile_cumulative_layout_shift', row.get('mobile_cumulative_layout_shift', 'N/A'))}">{row.get('mobile_cumulative_layout_shift', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('mobile_speed_index', row.get('mobile_speed_index', 'N/A'))}">{row.get('mobile_speed_index', 'N/A')}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div style="flex: 1; min-width: 300px;">
                    <h5 style="color: var(--psi-gray-700); margin: 16px 0 12px 0; font-size: 14px; font-weight: 500;">🖥️ Desktop</h5>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>FCP</th>
                                <th>LCP</th>
                                <th>TBT</th>
                                <th>CLS</th>
                                <th>SI</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span class="score {get_metric_class('desktop_first_contentful_paint', row.get('desktop_first_contentful_paint', 'N/A'))}">{row.get('desktop_first_contentful_paint', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('desktop_largest_contentful_paint', row.get('desktop_largest_contentful_paint', 'N/A'))}">{row.get('desktop_largest_contentful_paint', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('desktop_total_blocking_time', row.get('desktop_total_blocking_time', 'N/A'))}">{row.get('desktop_total_blocking_time', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('desktop_cumulative_layout_shift', row.get('desktop_cumulative_layout_shift', 'N/A'))}">{row.get('desktop_cumulative_layout_shift', 'N/A')}</span></td>
                                <td><span class="score {get_metric_class('desktop_speed_index', row.get('desktop_speed_index', 'N/A'))}">{row.get('desktop_speed_index', 'N/A')}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """

    # Add legend at the end
    html += """
        <!-- Legend - PageSpeed style -->
        <div class="legend">
            <p class="legend-title">Performance Score</p>
            <div>
                <span class="score score-good legend-item">90-100 Good</span>
                <span class="score score-average legend-item">50-89 Needs Improvement</span>
                <span class="score score-poor legend-item">0-49 Poor</span>
            </div>

            <div class="thresholds">
                <h4>Core Web Vitals Thresholds</h4>
                <div class="threshold-item">FCP (First Contentful Paint): Good &lt;1.8s, Needs Improvement 1.8-3.0s, Poor &gt;3.0s</div>
                <div class="threshold-item">LCP (Largest Contentful Paint): Good &lt;2.5s, Needs Improvement 2.5-4.0s, Poor &gt;4.0s</div>
                <div class="threshold-item">TBT (Total Blocking Time): Good &lt;200ms, Needs Improvement 200-600ms, Poor &gt;600ms</div>
                <div class="threshold-item">CLS (Cumulative Layout Shift): Good &lt;0.1, Needs Improvement 0.1-0.25, Poor &gt;0.25</div>
                <div class="threshold-item">SI (Speed Index): Good &lt;3.4s, Needs Improvement 3.4-5.8s, Poor &gt;5.8s</div>
            </div>
        </div>
    """

    return html


if __name__ == "__main__":
    generate_html_report()
