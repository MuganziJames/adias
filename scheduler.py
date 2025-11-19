"""
Task Scheduler Script
Schedules automated execution of ADIAS pipeline
"""
import schedule
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def run_adias():
    """Execute the ADIAS pipeline"""
    logger.info(f"Scheduled execution started at {datetime.now()}")
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running ADIAS pipeline...")
    
    try:
        # Run main.py
        result = subprocess.run(
            ['python', 'main.py'],
            cwd=config.BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Scheduled execution completed successfully")
            print("✓ Pipeline completed successfully")
        else:
            logger.error(f"Pipeline failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            print(f"✗ Pipeline failed. Check logs: {config.LOG_FILE}")
        
    except Exception as e:
        logger.error(f"Scheduled execution failed: {str(e)}", exc_info=True)
        print(f"✗ Error: {str(e)}")


def setup_schedule():
    """Configure the schedule based on config settings"""
    
    if config.SCHEDULE_FREQUENCY == "daily":
        schedule.every().day.at(config.SCHEDULE_TIME).do(run_adias)
        print(f"Scheduled daily execution at {config.SCHEDULE_TIME}")
        
    elif config.SCHEDULE_FREQUENCY == "weekly":
        schedule.every().monday.at(config.SCHEDULE_TIME).do(run_adias)
        print(f"Scheduled weekly execution (Mondays) at {config.SCHEDULE_TIME}")
        
    elif config.SCHEDULE_FREQUENCY == "monthly":
        # Run on first day of month
        def monthly_job():
            if datetime.now().day == 1:
                run_adias()
        
        schedule.every().day.at(config.SCHEDULE_TIME).do(monthly_job)
        print(f"Scheduled monthly execution (1st of month) at {config.SCHEDULE_TIME}")
    
    logger.info(f"Scheduler configured: {config.SCHEDULE_FREQUENCY} at {config.SCHEDULE_TIME}")


def main():
    """Main scheduler loop"""
    print("\n" + "="*60)
    print("ADIAS SCHEDULER - Automated Execution")
    print("="*60 + "\n")
    
    setup_schedule()
    
    print("\nScheduler is running. Press Ctrl+C to stop.\n")
    print(f"Next run: {schedule.next_run()}\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user.")
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
