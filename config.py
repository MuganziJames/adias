"""
Configuration settings for ADIAS
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
SCRIPTS_DIR = BASE_DIR / 'scripts'
REPORTS_DIR = BASE_DIR / 'reports'
LOGS_DIR = BASE_DIR / 'logs'
VIZ_DIR = BASE_DIR / 'visualizations'

# Data file paths
# Use sample data for testing (replace with real ITU files when available)
ITU_REGIONAL_FILE = DATA_DIR / 'sample_digital_inequality_data.xlsx'
# ITU_REGIONAL_FILE = DATA_DIR / 'ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx'
ITU_GENDER_FILE = DATA_DIR / 'IndividualsUsingInternetByGender_Jan2025.xlsx'

# Report settings
REPORT_TITLE = "Digital Inequality Assessment Report"
REPORT_AUTHOR = "ADIAS - Automated Digital Inequality Assessment System"

# Analysis thresholds
LOW_ACCESS_THRESHOLD = 40  # % - regions below this are flagged as underserved
RURAL_URBAN_GAP_THRESHOLD = 20  # % - significant disparity threshold

# Logging settings
LOG_FILE = LOGS_DIR / 'adias.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Schedule settings (cron format)
SCHEDULE_TIME = "09:00"  # Daily at 9 AM
SCHEDULE_FREQUENCY = "daily"  # Options: daily, weekly, monthly
