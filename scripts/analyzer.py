"""
Data Analysis Module
Computes digital inequality indicators and statistics
"""
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


class DigitalInequalityAnalyzer:
    """Analyzes digital inequality metrics"""
    
    def __init__(self, data):
        """
        Initialize analyzer with cleaned data
        
        Args:
            data: pd.DataFrame with digital access indicators
        """
        self.data = data
        self.results = {}
        
    def identify_underserved_regions(self, access_column='internet_access_percentage', 
                                    threshold=None):
        """
        Identify regions with low digital access
        
        Args:
            access_column: Column name for internet access percentage
            threshold: Access percentage below which region is underserved
            
        Returns:
            pd.DataFrame: Underserved regions
        """
        if threshold is None:
            threshold = config.LOW_ACCESS_THRESHOLD
        
        logger.info(f"Identifying regions with access below {threshold}%")
        
        # Find column that matches (case-insensitive)
        matching_cols = [col for col in self.data.columns 
                        if access_column.lower() in col.lower()]
        
        if not matching_cols:
            logger.warning(f"Column '{access_column}' not found")
            return pd.DataFrame()
        
        col = matching_cols[0]
        underserved = self.data[self.data[col] < threshold].copy()
        underserved = underserved.sort_values(by=col)
        
        self.results['underserved_regions'] = underserved
        logger.info(f"Found {len(underserved)} underserved regions")
        
        return underserved
    
    def calculate_rural_urban_gap(self, rural_col='rural_internet_access', 
                                   urban_col='urban_internet_access'):
        """
        Calculate gap between rural and urban internet access
        
        Args:
            rural_col: Rural access column name
            urban_col: Urban access column name
            
        Returns:
            pd.DataFrame: Regions with gap data
        """
        # Find matching columns
        rural_matches = [col for col in self.data.columns if rural_col.lower() in col.lower()]
        urban_matches = [col for col in self.data.columns if urban_col.lower() in col.lower()]
        
        if not rural_matches or not urban_matches:
            logger.warning("Rural/Urban columns not found")
            return pd.DataFrame()
        
        df = self.data.copy()
        df['rural_urban_gap'] = df[urban_matches[0]] - df[rural_matches[0]]
        df = df.sort_values(by='rural_urban_gap', ascending=False)
        
        significant_gap = df[df['rural_urban_gap'] > config.RURAL_URBAN_GAP_THRESHOLD]
        
        self.results['rural_urban_gap'] = df
        logger.info(f"Calculated rural-urban gap for {len(df)} regions")
        
        return df
    
    def compute_inequality_index(self, columns=None):
        """
        Compute composite digital inequality index
        
        Args:
            columns: List of indicator columns to include
            
        Returns:
            pd.DataFrame: Data with inequality index
        """
        if columns is None:
            # Use all numeric columns
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Normalize columns to 0-1 scale
        df = self.data.copy()
        normalized = pd.DataFrame()
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    normalized[col] = (df[col] - min_val) / (max_val - min_val)
        
        # Calculate mean normalized score (higher = better access)
        if len(normalized.columns) > 0:
            df['digital_access_score'] = normalized.mean(axis=1) * 100
            df['inequality_index'] = 100 - df['digital_access_score']  # Invert so higher = more inequality
        
        self.results['inequality_index'] = df
        logger.info("Computed composite inequality index")
        
        return df
    
    def analyze_regional_disparities(self, region_column='region', 
                                    indicator_columns=None):
        """
        Analyze disparities between regions
        
        Args:
            region_column: Column containing region names
            indicator_columns: Indicators to compare
            
        Returns:
            dict: Regional comparison statistics
        """
        if indicator_columns is None:
            indicator_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Find region column
        region_cols = [col for col in self.data.columns if region_column.lower() in col.lower()]
        
        if not region_cols:
            logger.warning(f"Region column '{region_column}' not found")
            return {}
        
        region_col = region_cols[0]
        
        # Calculate statistics by region
        regional_stats = {}
        
        for col in indicator_columns:
            if col in self.data.columns:
                stats = {
                    'mean': self.data[col].mean(),
                    'median': self.data[col].median(),
                    'std': self.data[col].std(),
                    'min': self.data[col].min(),
                    'max': self.data[col].max(),
                    'range': self.data[col].max() - self.data[col].min()
                }
                regional_stats[col] = stats
        
        self.results['regional_disparities'] = regional_stats
        logger.info(f"Analyzed regional disparities for {len(indicator_columns)} indicators")
        
        return regional_stats
    
    def get_top_bottom_regions(self, column, n=10):
        """
        Get top and bottom N regions by indicator
        
        Args:
            column: Indicator column
            n: Number of regions to return
            
        Returns:
            dict: {'top': DataFrame, 'bottom': DataFrame}
        """
        matching_cols = [col for col in self.data.columns if column.lower() in col.lower()]
        
        if not matching_cols:
            return {'top': pd.DataFrame(), 'bottom': pd.DataFrame()}
        
        col = matching_cols[0]
        
        top = self.data.nlargest(n, col)
        bottom = self.data.nsmallest(n, col)
        
        return {'top': top, 'bottom': bottom}
    
    def calculate_summary_statistics(self):
        """
        Calculate overall summary statistics
        
        Returns:
            dict: Summary statistics
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        summary = {
            'total_regions': len(self.data),
            'indicators': {}
        }
        
        for col in numeric_cols:
            summary['indicators'][col] = {
                'mean': float(self.data[col].mean()),
                'median': float(self.data[col].median()),
                'std': float(self.data[col].std()),
                'min': float(self.data[col].min()),
                'max': float(self.data[col].max())
            }
        
        self.results['summary'] = summary
        logger.info("Calculated summary statistics")
        
        return summary
    
    def get_analysis_results(self):
        """Return all analysis results"""
        return self.results


def main():
    """Test analysis module"""
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
        
        # Analyze
        analyzer = DigitalInequalityAnalyzer(clean_data)
        
        print("\n=== Digital Inequality Analysis ===\n")
        
        # Summary stats
        summary = analyzer.calculate_summary_statistics()
        print(f"Total regions analyzed: {summary['total_regions']}")
        print(f"Indicators analyzed: {len(summary['indicators'])}")
        
        # Underserved regions
        underserved = analyzer.identify_underserved_regions()
        print(f"\nUnderserved regions (access < {config.LOW_ACCESS_THRESHOLD}%): {len(underserved)}")
        
        print("\n✓ Analysis completed successfully")
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {str(e)}")


if __name__ == "__main__":
    main()
