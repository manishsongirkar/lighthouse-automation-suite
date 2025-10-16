# 🚀 Lighthouse Automation Suite

A comprehensive Python automation tool that analyzes website performance using Google Lighthouse via PageSpeed Insights and generates detailed reports.

## 📋 Features

- ✅ **Automated PageSpeed Analysis** - Tests multiple URLs automatically
- ✅ **Mobile & Desktop Scores** - Captures both device types
- ✅ **Core Web Vitals** - Extracts detailed performance metrics with color coding
- ✅ **Visual Dashboard** - Color-coded HTML reports with Google performance thresholds
- ✅ **Anti-Bot Protection** - Robust measures to avoid detection
- ✅ **Multiple Report Formats** - CSV, color-coded HTML dashboard, and console reports
- ✅ **Batch Processing** - Analyze hundreds of URLs with configurable delays
- ✅ **Smart URL Validation** - Validates URLs and handles malformed entries
- ✅ **Cross-Platform** - Dynamic paths work on Windows, macOS, and Linux
- ✅ **Error Handling** - Graceful failure recovery and detailed logging

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

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- Google Chrome browser
- Internet connection

### Installation

1. **Clone or download this project**
```bash
git clone <repository-url>
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

### Option 1: Run Complete Analysis Workflow
```bash
python run_analysis.py
```
This runs the full workflow: analysis → reports → opens dashboard

### Option 2: Run Individual Components

**Just the PageSpeed analysis:**
```bash
python main.py
```

**Generate text summary report:**
```bash
python generate_report.py
```

**Generate HTML dashboard:**
```bash
python generate_html_report.py
```

## 📊 Output Files

### 1. `pagespeed_results.csv`
- Raw data in CSV format
- Import into Excel/Google Sheets
- Contains all scores and metrics
- Machine-readable for further analysis

### 2. `pagespeed_report.html`
- Interactive web dashboard with **color-coded performance indicators**
- **Visual score representations** with Google performance thresholds
- **Green/Orange/Red color coding** for Core Web Vitals
- Mobile and desktop results side-by-side
- Summary cards with average metrics
- Professional styling and responsive design

### 3. Console Reports
- Summary statistics
- Performance issue alerts
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
pip install selenium webdriver-manager fake-useragent pandas
```

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
├── main.py                    # Core automation script
├── urls.txt                   # URLs to analyze (supports comments)
├── generate_report.py         # Text report generator with Core Web Vitals
├── generate_html_report.py    # Color-coded HTML dashboard generator
├── run_analysis.py           # Complete workflow runner
├── requirements.txt          # Python dependencies
├── packages.txt             # System dependencies
├── README.md                # Project documentation
├── SETUP.md                 # Detailed setup instructions
├── CORE_WEB_VITALS_UPDATE.md # Feature update documentation
├── .gitignore              # Git ignore rules
├── pagespeed_results.csv   # Generated results (gitignored)
└── pagespeed_report.html   # Generated color-coded dashboard (gitignored)
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

### October 2025 - Color-Coded Core Web Vitals
- ✅ **Color-coded HTML dashboard** with Google performance thresholds
- ✅ **Green/Orange/Red indicators** for instant performance identification
- ✅ **Professional styling** with responsive design
- ✅ **Enhanced URL validation** with detailed reporting
- ✅ **Cross-platform compatibility** with dynamic paths

See `CORE_WEB_VITALS_UPDATE.md` for detailed information about the latest enhancements.

---

**Happy Analyzing! 🎉**
