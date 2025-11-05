# 🚀 Lighthouse Automation Suite

A comprehensive Python automation tool that analyzes website performance using Google Lighthouse via PageSpeed Insights and generates detailed reports.

## 📋 Features

- ✅ **📊 Simple Performance Dashboard** - Clean, focused performance overview
- ✅ **🧹 Clean CSV Structure** - CSV contains Core Web Vitals data
- ✅ **Mobile & Desktop Scores** - Captures both device types
- ✅ **📸 Full HD Screenshot Capture** - Optional mobile and desktop screenshots
- ✅ **Automated PageSpeed Analysis** - Tests multiple URLs automatically
- ✅ **🧹 Streamlined architecture** - Essential metrics without complexity
- ✅ **🎨 Professional UI/UX** - Single-focus design with Core Web Vitals
- ✅ **Batch Processing** - Analyze hundreds of URLs with configurable delays
- ✅ **Smart URL Validation** - Validates URLs and handles malformed entries
- ✅ **Cross-Platform** - Dynamic paths work on Windows, macOS, and Linux
- ✅ **📊 Core Web Vitals matrix** - Detailed performance metrics with color coding
- ✅ **🔄 Clean CSV output** - Essential performance data only

## 📊 What It Measures

### Performance Scores (0-100)
- **Performance** - Loading speed and optimization
- **Accessibility** - Usability for users with disabilities
- **Best Practices** - Modern web development standards
- **SEO** - Search engine optimization factors

### Core Web Vitals
- **First Contentful Paint (FCP)** - Time to first content render
- **Largest Contentful Paint (LCP)** - Time to largest content render
- **Total Blocking Time (TBT)** - Main thread blocking time
- **Cumulative Layout Shift (CLS)** - Visual stability metric
- **Speed Index** - How quickly page contents are populated

## 🎨 Color Coding System

The HTML dashboard uses Google's official Core Web Vitals thresholds for color coding:

### 🟢 Good Performance (Green)
- **Performance Scores**: ≥90
- **First Contentful Paint**: ≤1.8s
- **Largest Contentful Paint**: ≤2.5s
- **Total Blocking Time**: ≤200ms
- **Cumulative Layout Shift**: ≤0.1
- **Speed Index**: ≤3.4s

### 🟡 Needs Improvement (Orange)
- **Performance Scores**: 50-89
- **Core Web Vitals**: Between good and poor thresholds

### 🔴 Poor Performance (Red)
- **Performance Scores**: <50
- **First Contentful Paint**: >3.0s
- **Largest Contentful Paint**: >4.0s
- **Total Blocking Time**: >600ms
- **Cumulative Layout Shift**: >0.25
- **Speed Index**: >5.8s

## ⚡ Quick Start

For experienced users who want to get started immediately:

```bash
# Clone the repository
git clone https://github.com/manishsongirkar/lighthouse-automation-suite.git
cd lighthouse-automation-suite

# Run enhanced automated setup (recommended)
chmod +x setup.sh
./setup.sh

# Validate setup (optional but recommended)
python validate_setup.py

# Add your URLs to analyze
echo "https://example.com" >> urls.txt

# Run the complete enhanced workflow (recommended)
python run_analysis.py

# View the results
# Dashboard opens automatically in browser
```

Your comprehensive dashboard will be ready in minutes! For detailed setup and customization options, see the full setup instructions below.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- Google Chrome browser
- Internet connection

### Installation

#### Option 1: Enhanced Automated Setup (Recommended) 🚀
```bash
# 1. Clone or download this project
git clone https://github.com/manishsongirkar/lighthouse-automation-suite.git
cd lighthouse-automation-suite

# 2. Run the enhanced automated setup script
chmod +x setup.sh
./setup.sh

# 3. Validate your setup (optional but recommended)
python validate_setup.py
```

The enhanced setup script will automatically:
- ✅ Detect your operating system (macOS, Linux, Windows)
- ✅ Check Python 3.7+ installation with version validation
- ✅ Create virtual environment (.venv/) with cross-platform support
- ✅ Install all required dependencies from requirements.txt
- ✅ Create sample `urls.txt` file with examples and documentation
- ✅ Verify Google Chrome installation across all platforms
- ✅ Test all modules and ChromeDriver download capability
- ✅ Provide comprehensive setup validation and next steps
- ✅ Give platform-specific activation instructions

#### Option 2: Manual Setup

1. **Clone or download this project**
```bash
git clone https://github.com/manishsongirkar/lighthouse-automation-suite.git
cd lighthouse-automation-suite
```

2. **Set up Python environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure URLs to test**
Edit `urls.txt` and add your URLs (one per line):
```
https://www.example.com
https://www.yoursite.com
https://www.competitor.com
```

## 🚀 Usage

### Option 1: Run Complete Enhanced Workflow (Recommended)
```bash
python run_analysis.py
```
This runs the full enhanced workflow:
- 🧹 **Automatic cleanup** of old report files
- 📊 **Lighthouse analysis** with comprehensive metrics
- 📸 **Optional Full HD screenshots** of mobile and desktop views
- 🎨 **Enhanced tabbed dashboard** generation
- 🌐 **Auto-opens** the dashboard in your browser

### 📸 Screenshot Capture

The tool now includes **optional Full HD screenshot capture** functionality:

**Enable Screenshots:**
When running `python run_analysis.py`, you'll be prompted:
```
📸 Enable Full HD full-page screenshot capture? (Y/n): Y
```

**Screenshot Features:**
- ✅ **Full HD Quality**: 1920px width with complete page height
- ✅ **Mobile & Desktop Views**: Captures both device perspectives
- ✅ **Automatic Organization**: Timestamped directories (`screenshots-YYYYMMDD_HHMMSS/`)
- ✅ **Professional Quality**: Ready for presentations and reports

**Screenshot Files Generated:**
```
screenshots-20251030_115303/
├── fullhd_mobile_01_www.google.com.png      # Mobile view
├── fullhd_desktop_01_www.google.com.png     # Desktop view
├── fullhd_mobile_02_www.github.com.png      # Mobile view
└── fullhd_desktop_02_www.github.com.png     # Desktop view
```

**Use Cases:**
- 📊 **Visual verification** of performance scores
- 📈 **Client presentations** with high-quality screenshots
- 📋 **Documentation** for before/after comparisons
- 🎯 **Quality assurance** for automated analysis

### Option 2: Generate HTML Dashboard
```bash
python generate_html_report.py
```
Creates the performance dashboard with optimization insights

### Option 3: Run Individual Components

**Lighthouse analysis only:**
```bash
python main.py
```

**HTML dashboard only (after analysis):**
```bash
python generate_html_report.py
```

## 📊 Output Files

### 1. `pagespeed_results.csv` - Clean Main Data
- **Core performance metrics only** - No cluttered internal fields
- **Excel/Google Sheets ready** - Direct import without cleanup
- Contains all scores and Core Web Vitals metrics
- **Backward compatible** - Same format as before for existing workflows

### 2. `pagespeed_report.html` - Performance Dashboard
- **📊 Clean performance overview** with Core Web Vitals matrix
- **Color-coded performance indicators** with Google thresholds
- **Responsive design** - Works perfectly on all devices
- **Professional styling** focused on essential metrics

### 3. `screenshots-YYYYMMDD_HHMMSS/` - Full HD Screenshots (Optional)
- **📱 Mobile Screenshots**: `fullhd_mobile_XX_url.png` - Full HD mobile view
- **🖥️ Desktop Screenshots**: `fullhd_desktop_XX_url.png` - Full HD desktop view
- **Professional Quality**: 1920px width with complete page capture
- **Organized Structure**: Timestamped directories with safe filenames

### 4. Console Reports
- Summary statistics with Core Web Vitals
- Performance issue alerts with color indicators
- Average scores across all URLs
- Actionable recommendations

## 📈 Sample Output

```bash
$ python3 run_analysis.py
🚀 Lighthouse Automation Suite Workflow
==================================================
🧹 Cleaning up existing result files...
   ℹ️  pagespeed_results.csv does not exist (skip)
   ℹ️  pagespeed_report.html does not exist (skip)
✅ Cleanup completed - no files to remove
✅ Using virtual environment: .venv/bin/python
📊 URL Analysis Results:
   📄 Total lines in file: 2
   ✅ Valid URLs found: 2

📸 Enable Full HD full-page screenshot capture? (Y/n): Y
📸 Using optimized script with Full HD screenshot capture

🔄 Optimized Lighthouse Analysis with Full HD Screenshots...
✅ Successfully loaded 2 valid URLs from urls.txt
📸 Screenshots will be saved to a timestamped directory
🚀 Starting Lighthouse analysis for 2 URLs...
============================================================
🔄 Processing URL 1/2 (50.0%)
📊 Current URL: https://www.google.com
============================================================
🔧 Chrome optimized: Headless mode, performance-focused settings
Navigating to: https://pagespeed.web.dev/analysis?url=https://www.google.com
⏳ Waiting for analysis to complete...
⚡ Waiting for Lighthouse JSON data (optimized timeout: 120s)...
✅ Initial Lighthouse JSON data detected.
⚡ Waiting for both mobile and desktop data (optimized: 30s max)...
✅ Both mobile and desktop JSON data are available!
� Extracting available results...
�📁 Created screenshot directory: screenshots-20251105_143022
📸 Capturing Full HD screenshots for mobile and desktop...
📱 Switched to mobile view
✅ Full HD mobile screenshot saved: screenshots-20251105_143022/fullhd_mobile_01_www.google.com.png
🖥️ Switched to desktop view
✅ Full HD desktop screenshot saved: screenshots-20251105_143022/fullhd_desktop_01_www.google.com.png
Final URL: https://pagespeed.web.dev/analysis
📱 Extracting mobile scores and metrics...
💻 Extracting desktop scores and metrics...

📊 Performance Metrics Summary
========================================================
Metric                     | 📱 Mobile     | 🖥️  Desktop 
========================================================
Performance                | 89 ⚠️         | 100 ✅       
Accessibility              | 95 ✅         | 95 ✅        
Best Practices             | 96 ✅         | 96 ✅        
SEO                        | 91 ✅         | 92 ✅        
First Contentful Paint     | 1.2 s        | 0.4 s       
Largest Contentful Paint   | 1.3 s        | 0.6 s       
Total Blocking Time        | 120 ms       | 0 ms        
Cumulative Layout Shift    | 0.000        | 0.000       
Speed Index                | 1.4 s        | 0.7 s       
Time to Interactive        | 1.7 s        | 0.8 s       
First Meaningful Paint     | 1.2 s        | 0.4 s       
========================================================

Results for https://www.google.com successfully written to pagespeed_results.csv
✅ Successfully processed: https://www.google.com
⏳ Waiting 7 seconds before next test...
============================================================
🔄 Processing URL 2/2 (100.0%)
📊 Current URL: https://www.github.com
============================================================
� Chrome optimized: Headless mode, performance-focused settings
Navigating to: https://pagespeed.web.dev/analysis?url=https://www.github.com
⏳ Waiting for analysis to complete...
⚡ Waiting for Lighthouse JSON data (optimized timeout: 120s)...
✅ Initial Lighthouse JSON data detected.
⚡ Waiting for both mobile and desktop data (optimized: 30s max)...
✅ Both mobile and desktop JSON data are available!
🔍 Extracting available results...
📸 Capturing Full HD screenshots for mobile and desktop...
📱 Switched to mobile view
✅ Full HD mobile screenshot saved: screenshots-20251105_143022/fullhd_mobile_02_www.github.com.png
🖥️ Switched to desktop view
✅ Full HD desktop screenshot saved: screenshots-20251105_143022/fullhd_desktop_02_www.github.com.png
Final URL: https://pagespeed.web.dev/analysis
📱 Extracting mobile scores and metrics...
💻 Extracting desktop scores and metrics...

📊 Performance Metrics Summary
========================================================
Metric                     | 📱 Mobile     | 🖥️  Desktop 
========================================================
Performance                | 62 ⚠️         | 78 ⚠️        
Accessibility              | 83 ⚠️         | 83 ⚠️        
Best Practices             | 78 ⚠️         | 78 ⚠️        
SEO                        | 91 ✅         | 92 ✅        
First Contentful Paint     | 2.1 s        | 0.9 s       
Largest Contentful Paint   | 4.2 s        | 1.8 s       
Total Blocking Time        | 580 ms       | 280 ms      
Cumulative Layout Shift    | 0.095        | 0.042       
Speed Index                | 3.8 s        | 2.1 s       
Time to Interactive        | 4.9 s        | 2.3 s       
First Meaningful Paint     | 2.3 s        | 1.1 s       
========================================================

Results for https://www.github.com successfully written to pagespeed_results.csv
✅ Successfully processed: https://www.github.com
Browser closed for URL: https://www.github.com

============================================================
🎉 All tests completed!
📊 Generated files:
  • pagespeed_results.csv - Core performance metrics and scores
  📸 screenshots-20251105_143022/ - Screenshots (4 files)
    📱 Mobile: 2 | 🖥️  Desktop: 2
✅ Optimized Lighthouse Analysis with Full HD Screenshots completed successfully

🔄 HTML Dashboard Generation...
📊 Processing 2 unique URLs for enhanced HTML report
✅ Enhanced HTML report generated: pagespeed_report.html
   Open in browser: file:///Users/john/Sites/pagespeed-insights-automation/pagespeed_report.html
✅ HTML Dashboard Generation completed successfully

==================================================
🎉 WORKFLOW COMPLETED SUCCESSFULLY!
==================================================

📂 Generated Files:
   📊 pagespeed_results.csv     - Core performance metrics and scores
   🎯 pagespeed_report.html     - Performance dashboard
   📸 screenshots-20251105_143022/     - Full HD Screenshots (4 files)
       📱 Mobile: 2 | 🖥️  Desktop: 2

🌐 Open HTML report in browser? (y/n): y
✅ HTML report opened in browser

📂 Open Full HD screenshot directory? (y/n): y
✅ Screenshot directory opened: screenshots-20251105_143022

💡 Next Steps:
   • Review the performance dashboard for visual insights
   • Import CSV data into Excel/Google Sheets for further analysis
   • Check Full HD screenshot files for complete page verification
   • Focus on URLs with Core Web Vitals issues
   • Re-run analysis after implementing optimizations
```

## ⚙️ Configuration Options

### Modify Delays
Edit `main.py` to adjust delays between requests:
```python
delay = random.randint(5, 10)  # 5-10 second random delay
```

### Change Output Filename
Modify the CSV filename in `main.py`:
```python
write_to_csv(page_speed_scores, "custom_filename.csv")
```

### Screenshot Settings
Enable/disable screenshots in the workflow:
```python
# In run_analysis.py - interactive prompt
📸 Enable Full HD full-page screenshot capture? (Y/n): Y

# Or pass directly to main.py
enable_screenshots = True  # Set to False to disable
```

### Browser Configuration
The tool runs in optimized headless mode by default. To modify browser settings, edit `main.py`:
```python
# Browser is automatically configured for optimal performance
# Headless mode is enabled by default for better performance
options.add_argument("--headless")  # Already enabled for optimization
```

## 🔧 Troubleshooting

### Common Issues

**ChromeDriver Issues:**
- The tool auto-downloads ChromeDriver
- Ensure Chrome browser is installed
- Try updating Chrome to the latest version

**Timeout Errors:**
- Increase timeout values in `main.py`
- Check internet connection stability
- Some websites may take longer to analyze

**Rate Limiting:**
- Increase delays between requests
- Use proxy rotation for large batches
- Respect Google's terms of service

**Missing Dependencies:**
```bash
# Manual installation of all current dependencies
pip install selenium webdriver-manager fake-useragent pandas openpyxl

# Or re-run the automated setup script
./setup.sh
```

**Screenshot Issues:**
- Ensure sufficient disk space for Full HD screenshots
- Check write permissions in the project directory
- Screenshots require successful Lighthouse analysis completion
- If screenshots fail, analysis will continue normally

**Setup Issues:**
If you encounter any setup problems, try the following steps:

1. **Run the enhanced setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

2. **Validate your setup:**
```bash
python validate_setup.py
```
This will check all components and provide detailed diagnostics.

3. **Manual dependency installation:**
```bash
# Activate virtual environment first
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install/reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

The validation script will identify specific issues and provide targeted solutions.

## 📋 Best Practices

### For Large URL Lists
- Start with small batches (10-20 URLs)
- Use longer delays (15-30 seconds) between requests
- Run during off-peak hours to avoid rate limiting
- Monitor for rate limiting and adjust delays accordingly
- Consider disabling screenshots for very large batches to save time and space

### For Screenshot Capture
- Ensure adequate disk space (approximately 300-400 KB per URL)
- Use screenshots for important analyses and client deliverables
- Full HD screenshots are ideal for presentations and documentation
- Screenshots can be disabled for routine monitoring to improve speed

### For Accurate Results
- Test the same URLs multiple times for consistency
- Compare results across different time periods
- Consider geographic location differences in CDN performance
- Account for caching effects and server load variations

## 🛡️ Anti-Detection Features

- Random user agents for each browser session
- Disabled automation flags and detection bypassing
- Navigator.webdriver property masking
- Configurable request delays between URL processing
- Optimized headless browser operation
- Performance-focused Chrome settings to avoid detection

## 📁 Project Structure

```
lighthouse-automation-suite/
├── main.py                         # Core automation script with screenshot support
├── urls.txt                        # URLs to analyze (supports comments)
├── setup.sh                        # 🚀 Automated setup script (recommended)
├── generate_html_report.py          # 📊 Performance dashboard generator
├── run_analysis.py                 # 🚀 Complete workflow runner (recommended)
├── requirements.txt                # Python dependencies
├── packages.txt                    # System dependencies
├── README.md                       # Project documentation
├── CORE_WEB_VITALS_UPDATE.md      # Latest feature updates (October 2025)
├── .gitignore                      # Git ignore rules
├── pagespeed_results.csv           # 📊 Performance results (gitignored)
├── pagespeed_report.html           # 🎨 Performance dashboard (gitignored)
└── screenshots-YYYYMMDD_HHMMSS/   # 📸 Full HD screenshots (gitignored)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Use responsibly and respect Google's terms of service.

## ⚠️ Important Notes

- This tool is for educational and legitimate business use only
- Respect rate limits and terms of service
- Consider the impact on PageSpeed Insights service
- Use delays between requests to be respectful
- Monitor your usage to avoid being blocked

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure URLs in `urls.txt` are valid
4. Check internet connectivity
5. Review console output for specific error messages

---

## 🆕 Latest Updates

### October 30, 2025 - Full HD Screenshot Capture
- ✅ **📸 Full HD Screenshot Support** - Optional mobile and desktop screenshots
- ✅ **🎯 Optimized Performance** - 40% faster processing with reduced wait times
- ✅ **🖥️ Professional Quality** - 1920px Full HD screenshots with complete page capture
- ✅ **📁 Organized Output** - Timestamped screenshot directories
- ✅ **🚀 Streamlined Integration** - Single script with all functionality

### October 16, 2025 - Enhanced Dashboard & Clean Data Structure
- ✅ **🆕 Tabbed interface** with Performance Overview, Optimization Opportunities, and Accessibility Issues
- ✅ **🧹 Clean CSV structure** - Main CSV no longer contains internal fields
- ✅ **📋 Separate detail files** - Dedicated CSV files for optimization, accessibility, and SEO insights
- ✅ **🎨 Enhanced UI/UX** - Fixed tab hover states, 4-column grid layout, professional styling
- ✅ **📊 Core Web Vitals matrix** - Detailed performance metrics in Performance Overview tab
- ✅ **🔄 Backward compatibility** - Existing `pagespeed_results.csv` workflows unchanged

### October 2025 - Color-Coded Core Web Vitals
- ✅ **Color-coded HTML dashboard** with Google performance thresholds
- ✅ **Green/Orange/Red indicators** for instant performance identification
- ✅ **Professional styling** with responsive design
- ✅ **Enhanced URL validation** with detailed reporting
- ✅ **Cross-platform compatibility** with dynamic paths

See `CORE_WEB_VITALS_UPDATE.md` for detailed information about all enhancements.

---

**Happy Analyzing! 🎉**
