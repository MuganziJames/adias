"""
PDF Report Generator Module
Creates automated PDF reports with charts and analysis
"""
from fpdf import FPDF
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DigitalInequalityReport(FPDF):
    """Custom PDF report for digital inequality analysis"""
    
    def __init__(self):
        super().__init__()
        self.title_text = config.REPORT_TITLE
        self.author_text = config.REPORT_AUTHOR
        
    def header(self):
        """Custom header for each page"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, self.title_text, 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Custom footer with page numbers"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        """Add a chapter title"""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(5)
        
    def chapter_body(self, text):
        """Add body text"""
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln()
        
    def add_table(self, df, title=""):
        """Add a data table to the report"""
        if title:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(2)
        
        # Check if dataframe is empty
        if df.empty:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'No data available', 0, 1, 'C')
            self.ln(5)
            return
        
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(200, 220, 255)
        
        # Calculate column widths based on content
        # Use fixed widths that fit on page
        num_cols = len(df.columns)
        available_width = 180  # Page width minus margins
        col_width = available_width / num_cols
        
        # Header
        for col in df.columns:
            col_text = str(col)[:25]  # Truncate long headers
            self.cell(col_width, 7, col_text, 1, 0, 'C', True)
        self.ln()
        
        # Data rows
        self.set_font('Arial', '', 8)
        for i, row in df.iterrows():
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    text = 'N/A'
                elif isinstance(value, float):
                    text = f'{value:.2f}'
                else:
                    text = str(value)[:25]  # Truncate long values
                self.cell(col_width, 6, text, 1, 0, 'C')
            self.ln()
        
        self.ln(5)


class ReportGenerator:
    """Generates complete PDF reports"""
    
    def __init__(self, analysis_results, charts, summary_stats):
        """
        Initialize report generator
        
        Args:
            analysis_results: Dictionary of analysis results
            charts: List of chart file paths
            summary_stats: Dictionary of summary statistics
        """
        self.analysis_results = analysis_results
        self.charts = charts
        self.summary_stats = summary_stats
        
    def generate_report(self, output_path=None):
        """
        Generate complete PDF report
        
        Args:
            output_path: Path to save PDF. Defaults to reports directory
            
        Returns:
            str: Path to generated report
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = config.REPORTS_DIR / f'digital_inequality_report_{timestamp}.pdf'
        
        logger.info(f"Generating report: {output_path}")
        
        pdf = DigitalInequalityReport()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Cover page
        self._add_cover_page(pdf)
        
        # Executive summary
        self._add_executive_summary(pdf)
        
        # Key findings
        self._add_key_findings(pdf)
        
        # Charts and visualizations
        self._add_visualizations(pdf)
        
        # Detailed statistics
        self._add_statistics(pdf)
        
        # Recommendations
        self._add_recommendations(pdf)
        
        # Save
        pdf.output(str(output_path))
        logger.info(f"Report saved: {output_path}")
        
        # Save a copy to root folder for easy testing (if enabled)
        if config.SAVE_LATEST_TO_ROOT:
            try:
                root_copy_path = config.BASE_DIR / 'latest_report.pdf'
                pdf.output(str(root_copy_path))
                logger.info(f"Copy saved to root: {root_copy_path}")
            except Exception as e:
                logger.warning(f"Could not save copy to root: {str(e)}")
        
        return str(output_path)
    
    def _add_cover_page(self, pdf):
        """Add cover page"""
        pdf.add_page()
        
        pdf.ln(60)
        pdf.set_font('Arial', 'B', 24)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 15, config.REPORT_TITLE, 0, 1, 'C')
        
        pdf.ln(10)
        pdf.set_font('Arial', '', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, 'SDG 10: Reduced Inequalities', 0, 1, 'C')
        
        pdf.ln(20)
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}', 0, 1, 'C')
        
        pdf.ln(10)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 10, config.REPORT_AUTHOR, 0, 1, 'C')
        
    def _add_executive_summary(self, pdf):
        """Add executive summary"""
        pdf.add_page()
        pdf.chapter_title('Executive Summary')
        
        total_regions = self.summary_stats.get('total_regions', 0)
        
        summary_text = f"""This report presents an automated analysis of digital inequality across {total_regions} regions worldwide. The analysis focuses on disparities in internet access, digital device ownership, and digital literacy - key factors that contribute to economic and social inequality.

Key areas examined:
- Internet access penetration rates
- Rural-urban digital divide
- Regional disparities in digital infrastructure
- Identification of underserved populations

The findings highlight significant gaps that require targeted policy interventions to ensure equitable digital access for all communities."""
        
        pdf.chapter_body(summary_text)
        
    def _add_key_findings(self, pdf):
        """Add key findings section"""
        pdf.chapter_title('Key Findings')
        
        # Finding 1: Underserved regions
        if 'underserved_regions' in self.analysis_results:
            underserved = self.analysis_results['underserved_regions']
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, f'1. Underserved Regions: {len(underserved)} identified', 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, f'Regions with internet access below {config.LOW_ACCESS_THRESHOLD}% require immediate attention.')
            pdf.ln(5)
        
        # Finding 2: Rural-urban gap
        if 'rural_urban_gap' in self.analysis_results:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, '2. Rural-Urban Digital Divide', 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, 'Significant disparities exist between urban and rural internet access, with rural areas consistently lagging behind.')
            pdf.ln(5)
        
        # Finding 3: Regional disparities
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, '3. Regional Disparities', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, 'Analysis reveals substantial variation in digital access across different geographic regions, indicating unequal distribution of digital infrastructure.')
        pdf.ln(5)
        
    def _add_visualizations(self, pdf):
        """Add charts and visualizations"""
        pdf.add_page()
        pdf.chapter_title('Data Visualizations')
        
        for chart_path in self.charts:
            if Path(chart_path).exists():
                try:
                    # Add chart title
                    chart_name = Path(chart_path).stem.replace('_', ' ').title()
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(0, 10, chart_name, 0, 1, 'L')
                    pdf.ln(2)
                    
                    # Add image
                    pdf.image(chart_path, x=10, w=190)
                    pdf.ln(10)
                    
                    logger.info(f"Added chart to report: {chart_path}")
                except Exception as e:
                    logger.warning(f"Could not add chart {chart_path}: {str(e)}")
        
    def _add_statistics(self, pdf):
        """Add detailed statistics tables"""
        pdf.add_page()
        pdf.chapter_title('Statistical Summary')
        
        if 'summary' in self.summary_stats:
            indicators = self.summary_stats['summary'].get('indicators', {})
            
            if indicators:
                # Create summary table
                stats_data = []
                for indicator, stats in list(indicators.items())[:10]:  # Limit to 10 indicators
                    stats_data.append({
                        'Indicator': indicator[:30],
                        'Mean': f"{stats['mean']:.2f}",
                        'Median': f"{stats['median']:.2f}",
                        'Min': f"{stats['min']:.2f}",
                        'Max': f"{stats['max']:.2f}"
                    })
                
                df = pd.DataFrame(stats_data)
                pdf.add_table(df, "Key Indicators Summary")
        
    def _add_recommendations(self, pdf):
        """Add recommendations section"""
        pdf.add_page()
        pdf.chapter_title('Recommendations')
        
        recommendations = """Based on the analysis, the following actions are recommended:

1. Infrastructure Investment
   - Prioritize broadband expansion in underserved regions
   - Improve rural connectivity through targeted infrastructure projects
   - Support public-private partnerships for digital infrastructure

2. Digital Literacy Programs
   - Implement community-based digital skills training
   - Integrate digital literacy into education curricula
   - Provide free or subsidized training for vulnerable populations

3. Affordability Initiatives
   - Subsidize internet access for low-income households
   - Promote affordable device financing programs
   - Support community technology centers

4. Policy Interventions
   - Develop national digital inclusion strategies
   - Monitor progress with regular assessments
   - Ensure regulatory frameworks promote equitable access

5. Data-Driven Monitoring
   - Continue automated assessment and reporting
   - Track progress against SDG 10 targets
   - Share insights with stakeholders for coordinated action"""
        
        pdf.chapter_body(recommendations)


def main():
    """Test report generation"""
    try:
        # Create sample report
        sample_stats = {
            'total_regions': 150,
            'summary': {
                'indicators': {
                    'internet_access': {'mean': 65.5, 'median': 70.0, 'min': 10.0, 'max': 98.0}
                }
            }
        }
        
        generator = ReportGenerator(
            analysis_results={},
            charts=[],
            summary_stats=sample_stats
        )
        
        report_path = generator.generate_report()
        print(f"\n✓ Report generated: {report_path}")
        
    except Exception as e:
        print(f"\n✗ Error generating report: {str(e)}")


if __name__ == "__main__":
    main()
