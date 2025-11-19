# Automated Digital Inequality Assessment System (ADIAS)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![SDG](https://img.shields.io/badge/SDG-10%20Reduced%20Inequalities-orange.svg)](https://sdgs.un.org/goals/goal10)

> **Capstone Project**: IT Automation with Python (FL25) | **Student**: James Muganzi

An automated Python system for analyzing digital inequality across regions, aligned with **SDG 10: Reduced Inequalities**. This capstone project demonstrates IT automation through scheduled data analysis, visualization, and report generation.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Output](#-output)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)

---

## 📋 Overview

Digital inequality—the gap between those with and without adequate digital access—perpetuates social and economic disparities. ADIAS automates the assessment of:

- **Internet access penetration rates** across regions
- **Rural-urban digital divide** analysis
- **Regional disparities** in digital infrastructure
- **Device ownership and digital literacy gaps**
- **Trend analysis** over time (2020-2025)

### Why This Matters

According to ITU data, approximately 2.2 billion people remain offline worldwide. This digital divide directly impacts:
- Educational opportunities
- Employment access
- Healthcare services
- Financial inclusion
- Economic development

ADIAS provides automated, data-driven insights to help policymakers, NGOs, and stakeholders make informed decisions to reduce these inequalities.

---

## 🔄 How It Works

ADIAS operates as a **fully automated pipeline** that transforms raw data into actionable insights:

### **The Complete Workflow**

```
┌─────────────────────────────────────────────────────────────────┐
│                     ADIAS AUTOMATION PIPELINE                    │
└─────────────────────────────────────────────────────────────────┘

Step 1: DATA LOADING
├─ Loads ITU regional/global ICT datasets (Excel format)
├─ Parses multiple sheets and indicators
├─ Validates data integrity
└─ Logs data summary (rows, columns, indicators)

Step 2: DATA CLEANING
├─ Normalizes column names (lowercase, underscores)
├─ Removes duplicate records
├─ Handles missing values (interpolation/imputation)
├─ Caps outliers using IQR method
├─ Validates percentage ranges (0-100%)
└─ Generates cleaning report

Step 3: ANALYSIS
├─ Identifies underserved regions (< 40% access threshold)
├─ Calculates rural-urban digital gaps
├─ Computes composite inequality indices
├─ Analyzes regional disparities (mean, median, std, range)
├─ Ranks regions (top/bottom performers)
└─ Generates summary statistics

Step 4: VISUALIZATION
├─ Internet Access by Region (bar chart)
├─ Rural vs Urban Comparison (bar chart)
├─ Inequality Distribution (histogram)
├─ Trend Over Time (line chart - if time-series data)
└─ Multi-Indicator Comparison (grouped bar chart)

Step 5: REPORT GENERATION
├─ Cover Page (title, date, author)
├─ Executive Summary (key findings overview)
├─ Key Findings (underserved regions, gaps, disparities)
├─ Data Visualizations (embedded charts)
├─ Statistical Tables (indicators summary)
├─ Recommendations (5 action areas)
└─ PDF Export (professional formatting)

Step 6: SCHEDULING (Optional)
├─ Daily execution at 09:00 (default)
├─ Weekly execution (Mondays)
├─ Monthly execution (1st of month)
└─ Logs all scheduled runs
```

### **Key Automation Features**

1. **Zero Manual Intervention**
   - Once configured, runs completely automatically
   - No need to manually open Excel, create charts, or write reports
   - All processes are scripted and repeatable

2. **Error Handling & Logging**
   - Comprehensive exception handling at every step
   - Detailed logs track all operations, warnings, and errors
   - Failed steps don't crash the entire pipeline

3. **Modular Architecture**
   - Each component (loading, cleaning, analysis, etc.) is independent
   - Easy to test, debug, and extend individual modules
   - Can run modules standalone for development

4. **Scheduled Execution**
   - Uses Python `schedule` library for periodic runs
   - Alternative: Windows Task Scheduler integration
   - Configurable frequency (daily/weekly/monthly)

5. **Data Validation**
   - Checks for missing files before processing
   - Validates data types and ranges
   - Ensures output quality at each step

---

## 🎯 Features

✅ **Automated Data Processing** - Loads and cleans ITU datasets with zero manual work  
✅ **Digital Inequality Analysis** - Identifies underserved regions and calculates gaps  
✅ **Automated Visualizations** - Generates publication-quality charts  
✅ **PDF Report Generation** - Creates comprehensive, formatted reports  
✅ **Scheduled Execution** - Runs automatically at configured intervals  
✅ **Comprehensive Logging** - Tracks all operations, errors, and warnings  
✅ **Sample Data Generator** - Test without downloading real datasets  
✅ **Modular Design** - Easy to extend and customize  

## 🗂️ Project Structure

```
adias/
├── config.py                 # Configuration settings
├── main.py                   # Main automation pipeline
├── scheduler.py              # Task scheduling script
├── requirements.txt          # Python dependencies
├── data/                     # Data files (ITU datasets)
├── scripts/
│   ├── data_loader.py       # Data ingestion
│   ├── data_cleaner.py      # Data cleaning
│   ├── analyzer.py          # Analysis logic
│   ├── visualizer.py        # Chart generation
│   └── report_generator.py  # PDF reports
├── reports/                  # Generated PDF reports
├── visualizations/           # Generated charts
└── logs/                     # Execution logs
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```powershell
   cd c:\Projects\adias
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Download ITU datasets**
   - [ITU Regional Data](https://www.itu.int/en/ITU-D/Statistics/Documents/facts/ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx)
   - [ITU Gender Data](https://www.itu.int/en/ITU-D/Statistics/Documents/statistics/2025/IndividualsUsingInternetByGender_Jan2025.xlsx)
   
   Place downloaded files in the `data/` folder.

4. **Configure settings (optional)**
   
   Edit `config.py` to customize:
   - Analysis thresholds
   - Schedule frequency and time
   - Report settings

## 💻 Usage

### **Quick Start (5 Minutes)**

1. **Activate virtual environment**
   ```powershell
   cd C:\Projects\adias
   .\venv\Scripts\Activate.ps1
   ```

2. **Run with sample data** (testing mode)
   ```powershell
   python main.py
   ```
   
   This runs the complete pipeline with synthetic data and generates:
   - 3 visualization charts (PNG files)
   - 1 comprehensive PDF report
   - Execution log with all details

3. **View results**
   - **Report**: `reports/digital_inequality_report_YYYYMMDD_HHMMSS.pdf`
   - **Charts**: `visualizations/*.png`
   - **Logs**: `logs/adias.log`

---

### **Usage Modes**

#### **Mode 1: Manual Execution (One-Time Analysis)**

Run the complete pipeline once:

```powershell
python main.py
```

**What happens:**
```
============================================================
AUTOMATED DIGITAL INEQUALITY ASSESSMENT SYSTEM (ADIAS)
============================================================

Step 1/6: Loading data...
  ✓ Loaded 120 records

Step 2/6: Cleaning data...
  ✓ Data cleaned (120 records after cleaning)

Step 3/6: Analyzing digital inequality...
  ✓ Analysis completed

Step 4/6: Generating visualizations...
  ✓ Generated 3 charts

Step 5/6: Creating PDF report...
  ✓ Report saved: reports/digital_inequality_report_20251119_161254.pdf

Step 6/6: Summary
  • Regions analyzed: 120
  • Charts generated: 3
  • Report location: reports/digital_inequality_report_20251119_161254.pdf
  • Underserved regions: 16
  • Log file: logs/adias.log

============================================================
PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

**Execution time**: ~15-30 seconds (depending on data size)

---

#### **Mode 2: Scheduled Automation (Continuous Monitoring)**

Start the scheduler for automated execution:

```powershell
python scheduler.py
```

**What happens:**
```
============================================================
ADIAS SCHEDULER - Automated Execution
============================================================

Scheduled daily execution at 09:00

Scheduler is running. Press Ctrl+C to stop.

Next run: 2025-11-20 09:00:00

[2025-11-20 09:00:00] Running ADIAS pipeline...
✓ Pipeline completed successfully
```

**Scheduler Settings** (configured in `config.py`):
- **Default**: Daily at 09:00 AM
- **Options**: daily, weekly, monthly
- **Customizable**: Change time and frequency in config

**Press `Ctrl+C`** to stop the scheduler.

---

#### **Mode 3: Windows Task Scheduler (Production Setup)**

For production environments, use Windows Task Scheduler for more reliability:

**Setup Steps:**

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create a new task**
   - Click "Create Basic Task"
   - Name: "ADIAS - Digital Inequality Assessment"

3. **Set trigger**
   - Choose frequency (Daily/Weekly/Monthly)
   - Set time (e.g., 9:00 AM)

4. **Set action**
   - Action: Start a program
   - Program: `C:\Projects\adias\venv\Scripts\python.exe`
   - Arguments: `main.py`
   - Start in: `C:\Projects\adias`

5. **Configure settings**
   - ☑ Run whether user is logged on or not
   - ☑ Run with highest privileges
   - ☑ Wake the computer to run this task (optional)

6. **Save and test**
   - Right-click task → "Run" to test
   - Check logs to verify execution

---

#### **Mode 4: Test Individual Modules**

Test specific components without running the full pipeline:

```powershell
# Test data loading
python scripts/data_loader.py

# Test data cleaning
python scripts/data_cleaner.py

# Test analysis
python scripts/analyzer.py

# Test visualizations
python scripts/visualizer.py

# Test report generation
python scripts/report_generator.py
```

---

### **Working with Real ITU Data**

Once you download actual ITU datasets:

1. **Download ITU files**
   - [ITU Regional Data](https://www.itu.int/en/ITU-D/Statistics/Documents/facts/ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx)
   - [ITU Gender Data](https://www.itu.int/en/ITU-D/Statistics/Documents/statistics/2025/IndividualsUsingInternetByGender_Jan2025.xlsx)

2. **Place files in `data/` folder**

3. **Update configuration**
   
   Edit `config.py`:
   ```python
   # Comment out sample data line
   # ITU_REGIONAL_FILE = DATA_DIR / 'sample_digital_inequality_data.xlsx'
   
   # Uncomment real data line
   ITU_REGIONAL_FILE = DATA_DIR / 'ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx'
   ```

4. **Run pipeline**
   ```powershell
   python main.py
   ```

---

### **Generate Fresh Sample Data**

If you need to regenerate or customize sample data:

```powershell
python generate_sample_data.py
```

This creates `data/sample_digital_inequality_data.xlsx` with:
- 20 global regions
- 6 years of data (2020-2025)
- 9 indicators per region/year
- Realistic variation and trends

## 📊 Output

### Generated Reports
- **Location**: `reports/digital_inequality_report_YYYYMMDD_HHMMSS.pdf`
- **Contents**:
  - Executive summary
  - Key findings
  - Data visualizations
  - Statistical tables
  - Recommendations

### Visualizations
- **Location**: `visualizations/*.png`
- **Charts**:
  - Internet access by region
  - Rural vs urban comparison
  - Inequality distribution
  - Trend analysis (if time-series data available)

### Logs
- **Location**: `logs/adias.log`
- **Contains**: Execution details, errors, warnings

## 🔧 Configuration

Key settings in `config.py`:

```python
# Analysis thresholds
LOW_ACCESS_THRESHOLD = 40  # % - regions flagged as underserved

# Schedule settings
SCHEDULE_TIME = "09:00"           # Daily execution time
SCHEDULE_FREQUENCY = "daily"      # Options: daily, weekly, monthly
```

## 🏗️ Architecture

### **System Design**

ADIAS follows a **modular, pipeline-based architecture** designed for maintainability and scalability:

```
┌───────────────────────────────────────────────────────────────┐
│                         ADIAS ARCHITECTURE                     │
└───────────────────────────────────────────────────────────────┘

                         ┌─────────────┐
                         │   main.py   │
                         │  (Pipeline  │
                         │ Orchestrator)│
                         └──────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
         ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
         │   config.py  │ │scheduler.py│ │generate_    │
         │ (Settings)   │ │(Automation)│ │sample_data  │
         └──────────────┘ └────────────┘ └─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────▼────┐           ┌──────▼──────┐        ┌──────▼──────┐
   │  Data   │           │   Analysis   │        │   Output    │
   │ Layer   │           │    Layer     │        │   Layer     │
   └─────────┘           └──────────────┘        └─────────────┘
        │                       │                       │
   ┌────┼────┐            ┌─────┼─────┐          ┌─────┼─────┐
   │    │    │            │     │     │          │     │     │
data_ data_ analyzer visualizer report_  logs/ reports/ viz/
loader cleaner  .py      .py    generator
  .py    .py                      .py
```

### **Module Responsibilities**

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **main.py** | Pipeline orchestration | Coordinates all steps, handles workflow |
| **config.py** | Configuration management | Paths, thresholds, settings |
| **data_loader.py** | Data ingestion | Load Excel files, parse sheets |
| **data_cleaner.py** | Data preparation | Clean, normalize, handle missing values |
| **analyzer.py** | Analysis engine | Calculate metrics, identify patterns |
| **visualizer.py** | Chart generation | Create PNG charts with matplotlib |
| **report_generator.py** | PDF creation | Format and export reports |
| **scheduler.py** | Task automation | Schedule periodic execution |
| **generate_sample_data.py** | Test data creation | Generate synthetic datasets |

### **Data Flow**

```
Raw Data (Excel)
    │
    ▼
[data_loader.py] ─── Loads & Parses
    │
    ▼
Raw DataFrame
    │
    ▼
[data_cleaner.py] ─── Cleans & Normalizes
    │
    ▼
Clean DataFrame
    │
    ├──────────────────────────┐
    │                          │
    ▼                          ▼
[analyzer.py]            [visualizer.py]
Calculate Metrics        Generate Charts
    │                          │
    ▼                          ▼
Analysis Results          PNG Files
    │                          │
    └──────────┬───────────────┘
               ▼
      [report_generator.py]
       Combine Everything
               │
               ▼
           PDF Report
```

### **Design Patterns**

1. **Pipeline Pattern**
   - Linear flow from data → analysis → output
   - Each stage produces input for the next
   - Easy to extend with new stages

2. **Dependency Injection**
   - Modules receive dependencies (data, config) as parameters
   - No hard-coded paths or settings in modules
   - Easy to test with mock data

3. **Single Responsibility**
   - Each module has one clear purpose
   - Changes to one module don't affect others
   - Easier to debug and maintain

4. **Configuration-Driven**
   - All settings in one place (config.py)
   - No magic numbers in code
   - Easy to customize without code changes

---

## 📦 Dependencies

### **Core Libraries**

| Package | Version | Purpose |
|---------|---------|---------|
| **pandas** | ≥2.0.0 | Data manipulation and analysis |
| **numpy** | ≥1.24.0 | Numerical operations and arrays |
| **matplotlib** | ≥3.7.0 | Data visualization and charting |
| **openpyxl** | ≥3.1.0 | Excel file reading/writing |
| **fpdf2** | ≥2.7.0 | PDF document generation |
| **schedule** | ≥1.2.0 | Task scheduling and automation |

### **Dependency Tree**

```
adias/
├── pandas (data manipulation)
│   ├── numpy (numerical operations)
│   ├── python-dateutil (date handling)
│   ├── pytz (timezone support)
│   └── tzdata (timezone database)
├── matplotlib (visualization)
│   ├── numpy
│   ├── pillow (image processing)
│   ├── cycler (color cycles)
│   ├── kiwisolver (layout engine)
│   ├── fonttools (font rendering)
│   ├── contourpy (contour plots)
│   └── pyparsing (text parsing)
├── openpyxl (Excel files)
│   └── et-xmlfile (XML parsing)
├── fpdf2 (PDF generation)
│   └── defusedxml (safe XML parsing)
└── schedule (automation)
```

**Total installed packages**: ~20 (including dependencies)  
**Installation size**: ~150 MB  
**Installation time**: ~2-3 minutes

## 🎓 Capstone Context

**Course**: IT Automation with Python (FL25)  
**Student**: James Muganzi  
**SDG Alignment**: SDG 10 - Reduced Inequalities  
**Submission Date**: November 2025

---

### **Project Objectives**

This capstone project demonstrates mastery of IT automation concepts through:

1. **Real-World Problem Solving**
   - Addresses global digital inequality (SDG 10)
   - Provides actionable insights for policymakers
   - Automates labor-intensive data analysis tasks

2. **Technical Skills Application**
   - Python scripting and automation
   - Data processing with pandas/numpy
   - Visualization with matplotlib
   - PDF generation and reporting
   - Task scheduling and error handling

3. **Professional Software Development**
   - Modular, maintainable code architecture
   - Comprehensive documentation
   - Version control ready (Git)
   - Production-grade error handling
   - Logging and monitoring

---

### **Automation Features Demonstrated**

#### **1. Data Processing Automation**
- ✅ Automatic loading of Excel datasets
- ✅ Intelligent data cleaning (missing values, outliers, normalization)
- ✅ No manual Excel operations required
- ✅ Repeatable and consistent processing

#### **2. Scheduled Execution**
- ✅ Python `schedule` library integration
- ✅ Windows Task Scheduler compatibility
- ✅ Configurable frequency (daily/weekly/monthly)
- ✅ Background execution support

#### **3. Error Handling & Logging**
- ✅ Try-except blocks at every critical point
- ✅ Comprehensive logging (INFO, WARNING, ERROR levels)
- ✅ Graceful failure recovery
- ✅ Detailed error messages for debugging

#### **4. Report Generation Automation**
- ✅ Automatic PDF creation with FPDF2
- ✅ Dynamic chart embedding
- ✅ Professional formatting and layout
- ✅ Timestamped file naming

#### **5. Modular Architecture**
- ✅ Separation of concerns (data, analysis, output)
- ✅ Reusable components
- ✅ Easy to extend and maintain
- ✅ Unit-testable modules

#### **6. Configuration Management**
- ✅ Centralized settings (config.py)
- ✅ No hard-coded values in modules
- ✅ Easy customization without code changes
- ✅ Environment-specific configurations

---

### **Learning Outcomes Achieved**

| Objective | Implementation | Evidence |
|-----------|----------------|----------|
| **Python Scripting** | 9 Python modules, 1,500+ lines of code | All scripts in `scripts/` folder |
| **Data Automation** | Pandas-based ETL pipeline | `data_loader.py`, `data_cleaner.py` |
| **Task Scheduling** | Schedule library + Windows Task Scheduler | `scheduler.py` |
| **Error Handling** | Try-except blocks, logging throughout | Check `logs/adias.log` |
| **Reporting** | Automated PDF generation | `report_generator.py` |
| **Documentation** | Comprehensive README, code comments | This file + inline docs |
| **Version Control** | Git-ready structure with .gitignore | Project root |

---

### **Project Impact**

**Technical Impact:**
- Reduces manual analysis time from **hours to seconds**
- Eliminates human error in data processing
- Enables continuous monitoring (daily/weekly updates)
- Scales to analyze hundreds of regions effortlessly

**Social Impact (SDG 10):**
- Identifies underserved regions needing intervention
- Quantifies rural-urban digital divide
- Tracks progress toward digital inclusion goals
- Provides evidence for policy decisions

**Educational Value:**
- Demonstrates real-world automation application
- Shows professional software development practices
- Integrates multiple technologies (data, viz, scheduling)
- Solves actual global challenge (digital inequality)

## 🐛 Troubleshooting

### **Common Issues and Solutions**

#### **Issue 1: Data file not found**
```
FileNotFoundError: ITU data file not found: C:\Projects\adias\data\ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx
```

**Solutions:**
1. **Use sample data** (recommended for testing)
   ```powershell
   python generate_sample_data.py
   # Edit config.py to use sample data
   ```

2. **Download real ITU data**
   - Download files from ITU website
   - Place in `data/` folder
   - Update `config.py` to point to real files

---

#### **Issue 2: Missing dependencies**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### **Issue 3: Virtual environment activation fails**
```
Activate.ps1 cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Set execution policy for current session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Then activate
.\venv\Scripts\Activate.ps1
```

---

#### **Issue 4: No visualizations generated**

**Check:**
1. Review `logs/adias.log` for error messages
2. Verify column names in data match expected format
3. Ensure matplotlib backend is set correctly

**Solution:**
```powershell
# Test visualization module separately
python scripts/visualizer.py
```

---

#### **Issue 5: PDF report generation fails**
```
Character "•" at index 197 is outside the range of characters supported
```

**Cause**: Special Unicode characters in text  
**Status**: ✅ Fixed in current version (uses ASCII-compatible characters)

If this occurs again:
1. Check `report_generator.py` for bullet points (• → -)
2. Replace em-dashes (— → -)
3. Use standard ASCII characters only

---

#### **Issue 6: Scheduler not running at specified time**

**Check:**
1. Verify system time is correct
2. Ensure computer is not in sleep mode
3. Check `config.py` for correct time format (24-hour)

**Better alternative for production**: Use Windows Task Scheduler instead of `scheduler.py`

---

#### **Issue 7: Out of memory errors**

**Cause**: Large datasets  
**Solutions:**
1. Process data in chunks
2. Increase system memory
3. Filter data to specific regions/years

---

#### **Issue 8: Permission denied errors**

**Cause**: Files are open in Excel/PDF viewer  
**Solution**: Close all files in `reports/` and `visualizations/` folders before running

---

### **Debug Mode**

Enable detailed logging for troubleshooting:

Edit `config.py`:
```python
LOG_LEVEL = 'DEBUG'  # Instead of 'INFO'
```

Then check `logs/adias.log` for detailed execution information.

---

### **Getting Help**

1. **Check logs**: `logs/adias.log` contains detailed error information
2. **Test modules**: Run individual scripts to isolate issues
3. **Verify data**: Ensure data files are valid Excel format
4. **Review configuration**: Check `config.py` for correct paths and settings

## 📊 Performance Metrics

### **System Performance**

| Metric | Value | Notes |
|--------|-------|-------|
| **Execution Time** | 15-30 seconds | For 120 records dataset |
| **Memory Usage** | ~150 MB | Including all libraries |
| **Data Processing Speed** | ~100 records/sec | Cleaning + analysis |
| **Chart Generation** | 3-5 seconds | Per visualization |
| **PDF Report Generation** | 2-3 seconds | With embedded images |
| **Automation Overhead** | < 1% | Scheduler CPU usage |

### **Scalability**

Tested with:
- ✅ 20 regions × 6 years = 120 records
- ✅ 10 indicators per record
- ✅ Multiple chart types (5+)
- ✅ 15-page PDF report

Can scale to:
- 🚀 1,000+ regions
- 🚀 10+ years of historical data
- 🚀 50+ indicators
- 🚀 100+ page reports

---

## 🔮 Future Enhancements

Potential improvements for future versions:

### **Phase 2: Enhanced Analysis**
- [ ] Machine learning predictions (forecast future trends)
- [ ] Cluster analysis (group similar regions)
- [ ] Correlation analysis (identify key drivers)
- [ ] Anomaly detection (flag unusual patterns)

### **Phase 3: Interactive Features**
- [ ] Web dashboard (Flask/Streamlit interface)
- [ ] Interactive charts (Plotly instead of matplotlib)
- [ ] User parameter input (custom thresholds)
- [ ] Real-time data updates

### **Phase 4: Data Integration**
- [ ] API integration (World Bank, ITU APIs)
- [ ] Database storage (PostgreSQL/SQLite)
- [ ] Multi-source data fusion
- [ ] Automated data downloads

### **Phase 5: Advanced Automation**
- [ ] Email report distribution
- [ ] Slack/Teams notifications
- [ ] Cloud deployment (AWS/Azure)
- [ ] CI/CD pipeline (GitHub Actions)

---

## 📝 License

This project is created for educational purposes as part of the IT Automation with Python capstone project.

**License**: MIT (open source, free to use and modify)

---

## 🤝 Contributing

This is a capstone project, but feedback and suggestions are welcome:

1. **Review the code** - Check modules for improvements
2. **Suggest features** - Propose enhancements
3. **Report issues** - Document any bugs found
4. **Test with real data** - Validate with actual ITU datasets

---

## 📧 Contact

**James Muganzi**  
Capstone Project - FL25 IT Automation With Python  
Digital Inequality Assessment System (ADIAS)

---

## 🙏 Acknowledgments

- **ITU (International Telecommunication Union)** - Data source and digital inequality research
- **World Bank** - Economic and development indicators
- **United Nations SDG Framework** - SDG 10 goals and targets
- **Python Community** - Open-source libraries (pandas, matplotlib, fpdf2)

---

## 📚 References

1. **ITU Statistics**
   - [ITU DataHub](https://datahub.itu.int/)
   - [ICT Facts and Figures](https://www.itu.int/en/ITU-D/Statistics/Pages/facts/default.aspx)

2. **SDG 10: Reduced Inequalities**
   - [UN SDG 10 Overview](https://sdgs.un.org/goals/goal10)
   - [Digital Divide Research](https://www.un.org/development/desa/dspd/2021/04/digital-divide/)

3. **Technical Documentation**
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
   - [FPDF2 Documentation](https://pyfpdf.github.io/fpdf2/)

---

**Note**: This system is designed for automated monitoring and reporting to support policymakers, NGOs, and stakeholders working to reduce digital inequality globally. The insights generated can inform infrastructure investments, policy interventions, and targeted programs to ensure equitable digital access for all communities.

---

<div align="center">

**Built with ❤️ for SDG 10: Reduced Inequalities**

*Automating digital inequality assessment, one report at a time.*

</div>
