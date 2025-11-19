"""
Main Automation Pipeline
Orchestrates the complete digital inequality analysis workflow
"""
import sys
from pathlib import Path
import logging
from datetime import datetime

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / 'scripts'))

import config
from scripts.data_loader import DataLoader
from scripts.data_cleaner import DataCleaner
from scripts.analyzer import DigitalInequalityAnalyzer
from scripts.visualizer import DigitalInequalityVisualizer
from scripts.report_generator import ReportGenerator

# Setup logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class ADIASPipeline:
    """Automated Digital Inequality Assessment System Pipeline"""
    
    def __init__(self):
        self.loader = None
        self.cleaner = None
        self.analyzer = None
        self.visualizer = None
        self.report_generator = None
        
        self.raw_data = None
        self.clean_data = None
        self.analysis_results = None
        self.charts = []
        self.report_path = None
        
    def run(self):
        """Execute the complete pipeline"""
        try:
            logger.info("="*60)
            logger.info("ADIAS Pipeline Started")
            logger.info(f"Timestamp: {datetime.now()}")
            logger.info("="*60)
            
            print("\n" + "="*60)
            print("AUTOMATED DIGITAL INEQUALITY ASSESSMENT SYSTEM (ADIAS)")
            print("="*60 + "\n")
            
            # Step 1: Load Data
            print("Step 1/6: Loading data...")
            self._load_data()
            print(f"  ✓ Loaded {len(self.raw_data)} records\n")
            
            # Step 2: Clean Data
            print("Step 2/6: Cleaning data...")
            self._clean_data()
            print(f"  ✓ Data cleaned ({len(self.clean_data)} records after cleaning)\n")
            
            # Step 3: Analyze
            print("Step 3/6: Analyzing digital inequality...")
            self._analyze_data()
            print("  ✓ Analysis completed\n")
            
            # Step 4: Visualize
            print("Step 4/6: Generating visualizations...")
            self._create_visualizations()
            print(f"  ✓ Generated {len(self.charts)} charts\n")
            
            # Step 5: Generate Report
            print("Step 5/6: Creating PDF report...")
            self._generate_report()
            print(f"  ✓ Report saved: {self.report_path}\n")
            
            # Step 6: Summary
            print("Step 6/6: Summary")
            self._print_summary()
            
            logger.info("ADIAS Pipeline Completed Successfully")
            print("\n" + "="*60)
            print("PIPELINE COMPLETED SUCCESSFULLY")
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            print(f"\n✗ ERROR: {str(e)}\n")
            print("Check logs for details: ", config.LOG_FILE)
            return False
    
    def _load_data(self):
        """Load ITU datasets"""
        self.loader = DataLoader()
        
        # Check if data files exist
        if not config.ITU_REGIONAL_FILE.exists():
            raise FileNotFoundError(
                f"ITU data file not found: {config.ITU_REGIONAL_FILE}\n"
                f"Please download the data file and place it in the data/ folder."
            )
        
        self.raw_data = self.loader.load_itu_regional_data()
        
        # Try to load gender data if available
        if config.ITU_GENDER_FILE.exists():
            self.loader.load_itu_gender_data()
        
        logger.info(f"Loaded data: {self.raw_data.shape}")
    
    def _clean_data(self):
        """Clean and prepare data"""
        self.cleaner = DataCleaner(self.raw_data)
        
        # Apply cleaning steps
        self.cleaner.normalize_column_names()
        self.cleaner.remove_duplicates()
        self.cleaner.handle_missing_values(strategy='interpolate')
        
        self.clean_data = self.cleaner.get_cleaned_data()
        
        # Log cleaning report
        for action in self.cleaner.get_cleaning_report():
            logger.info(f"Cleaning: {action}")
    
    def _analyze_data(self):
        """Perform analysis"""
        self.analyzer = DigitalInequalityAnalyzer(self.clean_data)
        
        # Run various analyses
        self.analyzer.identify_underserved_regions()
        self.analyzer.calculate_summary_statistics()
        
        # Try rural-urban analysis if columns exist
        try:
            self.analyzer.calculate_rural_urban_gap()
        except:
            logger.info("Rural-urban analysis skipped (columns not found)")
        
        self.analysis_results = self.analyzer.get_analysis_results()
    
    def _create_visualizations(self):
        """Generate charts"""
        self.visualizer = DigitalInequalityVisualizer(self.clean_data)
        
        # Generate available charts
        try:
            chart = self.visualizer.plot_internet_access_by_region()
            if chart:
                self.charts.append(chart)
        except Exception as e:
            logger.warning(f"Could not create access chart: {str(e)}")
        
        try:
            chart = self.visualizer.plot_inequality_distribution()
            if chart:
                self.charts.append(chart)
        except Exception as e:
            logger.warning(f"Could not create distribution chart: {str(e)}")
        
        try:
            chart = self.visualizer.plot_rural_urban_comparison()
            if chart:
                self.charts.append(chart)
        except Exception as e:
            logger.warning(f"Could not create rural-urban chart: {str(e)}")
    
    def _generate_report(self):
        """Create PDF report"""
        # Get full summary including all indicator statistics
        summary_stats = self.analysis_results.get('summary', {})
        
        # Ensure we have at least total_regions
        if 'total_regions' not in summary_stats:
            summary_stats['total_regions'] = len(self.clean_data)
        
        self.report_generator = ReportGenerator(
            analysis_results=self.analysis_results,
            charts=self.charts,
            summary_stats={'summary': summary_stats}  # Wrap in expected structure
        )
        
        self.report_path = self.report_generator.generate_report()
    
    def _print_summary(self):
        """Print execution summary"""
        summary = self.analysis_results.get('summary', {})
        total_regions = summary.get('total_regions', len(self.clean_data))
        
        print(f"  • Regions analyzed: {total_regions}")
        print(f"  • Charts generated: {len(self.charts)}")
        print(f"  • Report location: {self.report_path}")
        
        if 'underserved_regions' in self.analysis_results:
            underserved_count = len(self.analysis_results['underserved_regions'])
            print(f"  • Underserved regions: {underserved_count}")
        
        print(f"  • Log file: {config.LOG_FILE}")


def main():
    """Main entry point"""
    pipeline = ADIASPipeline()
    success = pipeline.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
