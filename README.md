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

# Run automated setup (recommended)
chmod +x setup.sh
./setup.sh

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

#### Option 1: Automated Setup (Recommended) 🚀
```bash
# 1. Clone or download this project
git clone https://github.com/manishsongirkar/lighthouse-automation-suite.git
cd lighthouse-automation-suite

# 2. Run the automated setup script
chmod +x setup.sh
./setup.sh
```

The setup script will automatically:
- ✅ Check Python 3.7+ installation
- ✅ Create virtual environment (.venv/)
- ✅ Install all required dependencies
- ✅ Create sample `urls.txt` file
- ✅ Verify Google Chrome installation
- ✅ Test all modules for proper installation

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

```
📊 PAGESPEED INSIGHTS ANALYSIS REPORT
================================================================================
Generated on: 2025-10-14 14:13:42
Total URLs Analyzed: 2

📱 MOBILE PERFORMANCE SCORES
----------------------------------------
https://www.google.com              | Perf:  85 | Acc:  91 | BP:  93 | SEO:  73
https://www.github.com              | Perf:  45 | Acc:  97 | BP:  96 | SEO: 100

🖥️  DESKTOP PERFORMANCE SCORES
----------------------------------------
https://www.google.com              | Perf:  92 | Acc:  91 | BP:  93 | SEO:  73
https://www.github.com              | Perf:  65 | Acc:  97 | BP:  96 | SEO: 100

⚡ CORE WEB VITALS SUMMARY
--------------------------------------------------
📱 MOBILE METRICS:
  First Contentful Paint   : 2.0s
  Largest Contentful Paint : 4.2s
  Total Blocking Time      : 650ms
  Cumulative Layout Shift  : 0.12
  Speed Index              : 4.5s

🖥️  DESKTOP METRICS:
  First Contentful Paint   : 950ms
  Largest Contentful Paint : 2.4s
  Total Blocking Time      : 460ms
  Cumulative Layout Shift  : 0.09
  Speed Index              : 2.7s

⚠️  PERFORMANCE ISSUES (Scores < 90)
--------------------------------------------------
https://www.github.com:
  ❌ Mobile Performance: 45
  ❌ Desktop Performance: 65
  🟠 Mobile LCP: 5.2s (Poor - exceeds 4.0s threshold)
  🟠 Mobile TBT: 850ms (Poor - exceeds 600ms threshold)
```

## ⚙️ Configuration Options

### Modify Delays
Edit `main.py` line ~280 to adjust delays between requests:
```python
delay = random.randint(5, 10)  # 5-10 second random delay
```

### Change Output Filename
Modify the CSV filename in `main.py`:
```python
write_to_csv(page_speed_scores, "custom_filename.csv")
```

### Headless Mode
Toggle browser visibility in `main.py`:
```python
# options.add_argument("--headless")  # Comment out to see browser
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
# Manual installation
pip install selenium webdriver-manager fake-useragent pandas

# Or re-run the automated setup script
./setup.sh
```

**Setup Issues:**
If you encounter any setup problems, try running the automated setup script:
```bash
chmod +x setup.sh
./setup.sh
```
This will verify your environment and reinstall all dependencies.

## 📋 Best Practices

### For Large URL Lists
- Start with small batches (10-20 URLs)
- Use longer delays (15-30 seconds)
- Run during off-peak hours
- Monitor for rate limiting

### For Accurate Results
- Test the same URLs multiple times
- Compare results across different time periods
- Consider geographic location differences
- Account for CDN and caching effects

## 🛡️ Anti-Detection Features

- Random user agents
- Disabled automation flags
- Navigator.webdriver property masking
- Configurable request delays
- Headless browser operation

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
