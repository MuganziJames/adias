"""
Visualization Module
Generates charts and graphs for digital inequality analysis
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for automation
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DigitalInequalityVisualizer:
    """Creates visualizations for digital inequality data"""
    
    def __init__(self, data, output_dir=None):
        """
        Initialize visualizer
        
        Args:
            data: pd.DataFrame with analysis results
            output_dir: Directory to save charts
        """
        self.data = data
        self.output_dir = output_dir or config.VIZ_DIR
        self.charts = []
        
        # Set style
        plt.style.use('ggplot')
        
    def plot_internet_access_by_region(self, access_column='internet_access_percentage',
                                       region_column='region', top_n=15):
        """
        Bar chart of internet access by region
        
        Args:
            access_column: Internet access percentage column
            region_column: Region name column
            top_n: Number of regions to display
            
        Returns:
            str: Path to saved chart
        """
        # Find matching columns
        access_cols = [col for col in self.data.columns if access_column.lower() in col.lower()]
        region_cols = [col for col in self.data.columns if region_column.lower() in col.lower()]
        
        if not access_cols:
            logger.warning(f"Access column not found")
            return None
        
        access_col = access_cols[0]
        region_col = region_cols[0] if region_cols else self.data.columns[0]
        
        # Get top and bottom regions
        df_sorted = self.data.sort_values(by=access_col)
        bottom = df_sorted.head(top_n // 2)
        top = df_sorted.tail(top_n // 2)
        plot_data = pd.concat([bottom, top])
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = ['#d62728' if x < config.LOW_ACCESS_THRESHOLD else '#2ca02c' 
                 for x in plot_data[access_col]]
        
        ax.barh(range(len(plot_data)), plot_data[access_col], color=colors)
        ax.set_yticks(range(len(plot_data)))
        ax.set_yticklabels(plot_data[region_col], fontsize=9)
        ax.set_xlabel('Internet Access (%)', fontsize=12)
        ax.set_title('Internet Access by Region\n(Top and Bottom Regions)', 
                    fontsize=14, fontweight='bold')
        ax.axvline(x=config.LOW_ACCESS_THRESHOLD, color='red', 
                  linestyle='--', linewidth=2, label=f'Threshold ({config.LOW_ACCESS_THRESHOLD}%)')
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_dir / 'internet_access_by_region.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.charts.append(str(output_path))
        logger.info(f"Saved chart: {output_path}")
        
        return str(output_path)
    
    def plot_rural_urban_comparison(self, rural_col='rural_internet_access',
                                    urban_col='urban_internet_access'):
        """
        Comparison chart of rural vs urban internet access
        
        Returns:
            str: Path to saved chart
        """
        # Find columns
        rural_matches = [col for col in self.data.columns if rural_col.lower() in col.lower()]
        urban_matches = [col for col in self.data.columns if urban_col.lower() in col.lower()]
        
        if not rural_matches or not urban_matches:
            logger.warning("Rural/Urban columns not found")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        rural_mean = self.data[rural_matches[0]].mean()
        urban_mean = self.data[urban_matches[0]].mean()
        
        categories = ['Rural', 'Urban']
        values = [rural_mean, urban_mean]
        colors = ['#ff7f0e', '#1f77b4']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        gap = urban_mean - rural_mean
        ax.set_ylabel('Internet Access (%)', fontsize=12)
        ax.set_title(f'Rural vs Urban Internet Access\nGap: {gap:.1f}%', 
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'rural_urban_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.charts.append(str(output_path))
        logger.info(f"Saved chart: {output_path}")
        
        return str(output_path)
    
    def plot_inequality_distribution(self, column='internet_access_percentage'):
        """
        Histogram showing distribution of digital access
        
        Returns:
            str: Path to saved chart
        """
        matching_cols = [col for col in self.data.columns if column.lower() in col.lower()]
        
        if not matching_cols:
            logger.warning(f"Column '{column}' not found")
            return None
        
        col = matching_cols[0]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(self.data[col].dropna(), bins=20, color='#9467bd', 
               alpha=0.7, edgecolor='black')
        ax.axvline(x=self.data[col].mean(), color='red', 
                  linestyle='--', linewidth=2, label=f'Mean: {self.data[col].mean():.1f}%')
        ax.axvline(x=self.data[col].median(), color='green', 
                  linestyle='--', linewidth=2, label=f'Median: {self.data[col].median():.1f}%')
        
        ax.set_xlabel('Internet Access (%)', fontsize=12)
        ax.set_ylabel('Number of Regions', fontsize=12)
        ax.set_title('Distribution of Internet Access Across Regions', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'inequality_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.charts.append(str(output_path))
        logger.info(f"Saved chart: {output_path}")
        
        return str(output_path)
    
    def plot_trend_over_time(self, time_column='year', 
                            indicator_column='internet_access_percentage'):
        """
        Line chart showing trend over time
        
        Returns:
            str: Path to saved chart
        """
        time_cols = [col for col in self.data.columns if time_column.lower() in col.lower()]
        indicator_cols = [col for col in self.data.columns if indicator_column.lower() in col.lower()]
        
        if not time_cols or not indicator_cols:
            logger.warning("Time or indicator column not found")
            return None
        
        time_col = time_cols[0]
        indicator_col = indicator_cols[0]
        
        # Group by time and calculate mean
        trend_data = self.data.groupby(time_col)[indicator_col].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(trend_data[time_col], trend_data[indicator_col], 
               marker='o', linewidth=2, markersize=8, color='#1f77b4')
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Internet Access (%)', fontsize=12)
        ax.set_title('Digital Access Trend Over Time', 
                    fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'trend_over_time.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.charts.append(str(output_path))
        logger.info(f"Saved chart: {output_path}")
        
        return str(output_path)
    
    def plot_top_indicators_comparison(self, indicators, region_column='region', top_n=10):
        """
        Multi-indicator comparison chart
        
        Args:
            indicators: List of indicator column names
            region_column: Region name column
            top_n: Number of regions to show
            
        Returns:
            str: Path to saved chart
        """
        region_cols = [col for col in self.data.columns if region_column.lower() in col.lower()]
        region_col = region_cols[0] if region_cols else self.data.columns[0]
        
        # Get top regions by first indicator
        df_sorted = self.data.nlargest(top_n, indicators[0])
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x = np.arange(len(df_sorted))
        width = 0.8 / len(indicators)
        
        for i, indicator in enumerate(indicators):
            if indicator in self.data.columns:
                offset = width * i - (width * len(indicators) / 2)
                ax.bar(x + offset, df_sorted[indicator], width, 
                      label=indicator.replace('_', ' ').title())
        
        ax.set_xlabel('Region', fontsize=12)
        ax.set_ylabel('Access (%)', fontsize=12)
        ax.set_title(f'Multi-Indicator Comparison (Top {top_n} Regions)', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df_sorted[region_col], rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'indicators_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.charts.append(str(output_path))
        logger.info(f"Saved chart: {output_path}")
        
        return str(output_path)
    
    def get_generated_charts(self):
        """Return list of generated chart paths"""
        return self.charts


def main():
    """Test visualization module"""
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    
    try:
        # Load and clean data
        loader = DataLoader()
        df = loader.load_itu_regional_data()
        
        cleaner = DataCleaner(df)
        cleaner.normalize_column_names()
        cleaner.handle_missing_values()
        clean_data = cleaner.get_cleaned_data()
        
        # Create visualizations
        visualizer = DigitalInequalityVisualizer(clean_data)
        
        print("\n=== Generating Visualizations ===\n")
        
        visualizer.plot_internet_access_by_region()
        visualizer.plot_inequality_distribution()
        
        charts = visualizer.get_generated_charts()
        print(f"\n✓ Generated {len(charts)} charts:")
        for chart in charts:
            print(f"  - {chart}")
        
    except Exception as e:
        print(f"\n✗ Error during visualization: {str(e)}")


if __name__ == "__main__":
    main()
