"""
Data Cleaning Module
Handles missing values, outliers, and data quality issues
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


class DataCleaner:
    """Cleans and prepares data for analysis"""
    
    def __init__(self, data):
        """
        Initialize cleaner with data
        
        Args:
            data: pd.DataFrame to clean
        """
        self.raw_data = data.copy()
        self.clean_data = data.copy()
        self.cleaning_report = []
        
    def handle_missing_values(self, strategy='interpolate', columns=None):
        """
        Handle missing values in dataset
        
        Args:
            strategy: 'drop', 'mean', 'median', 'interpolate', 'forward_fill'
            columns: Specific columns to process. None = all numeric columns
        """
        logger.info(f"Handling missing values using strategy: {strategy}")
        
        if columns is None:
            columns = self.clean_data.select_dtypes(include=[np.number]).columns
        
        missing_before = self.clean_data[columns].isnull().sum().sum()
        
        for col in columns:
            missing_count = self.clean_data[col].isnull().sum()
            
            if missing_count > 0:
                if strategy == 'drop':
                    self.clean_data = self.clean_data.dropna(subset=[col])
                elif strategy == 'mean':
                    self.clean_data[col].fillna(self.clean_data[col].mean(), inplace=True)
                elif strategy == 'median':
                    self.clean_data[col].fillna(self.clean_data[col].median(), inplace=True)
                elif strategy == 'interpolate':
                    self.clean_data[col] = self.clean_data[col].interpolate(method='linear')
                elif strategy == 'forward_fill':
                    self.clean_data[col].fillna(method='ffill', inplace=True)
                
                self.cleaning_report.append(f"Filled {missing_count} missing values in '{col}' using {strategy}")
        
        missing_after = self.clean_data[columns].isnull().sum().sum()
        logger.info(f"Missing values reduced from {missing_before} to {missing_after}")
        
    def remove_duplicates(self, subset=None):
        """
        Remove duplicate rows
        
        Args:
            subset: Columns to check for duplicates. None = all columns
        """
        before_count = len(self.clean_data)
        self.clean_data = self.clean_data.drop_duplicates(subset=subset, keep='first')
        after_count = len(self.clean_data)
        
        removed = before_count - after_count
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")
            self.cleaning_report.append(f"Removed {removed} duplicate rows")
    
    def handle_outliers(self, columns=None, method='iqr', threshold=1.5):
        """
        Detect and handle outliers
        
        Args:
            columns: Columns to check. None = all numeric
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier or z-score threshold
        """
        if columns is None:
            columns = self.clean_data.select_dtypes(include=[np.number]).columns
        
        outliers_removed = 0
        
        for col in columns:
            if method == 'iqr':
                Q1 = self.clean_data[col].quantile(0.25)
                Q3 = self.clean_data[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outliers = ((self.clean_data[col] < lower_bound) | 
                           (self.clean_data[col] > upper_bound))
                
                # Cap outliers instead of removing
                self.clean_data.loc[self.clean_data[col] < lower_bound, col] = lower_bound
                self.clean_data.loc[self.clean_data[col] > upper_bound, col] = upper_bound
                
                outliers_removed += outliers.sum()
        
        if outliers_removed > 0:
            logger.info(f"Capped {outliers_removed} outlier values")
            self.cleaning_report.append(f"Capped {outliers_removed} outliers using {method} method")
    
    def convert_data_types(self, type_mapping):
        """
        Convert column data types
        
        Args:
            type_mapping: dict {column_name: target_type}
        """
        for col, dtype in type_mapping.items():
            if col in self.clean_data.columns:
                try:
                    self.clean_data[col] = self.clean_data[col].astype(dtype)
                    logger.info(f"Converted '{col}' to {dtype}")
                except Exception as e:
                    logger.warning(f"Could not convert '{col}' to {dtype}: {str(e)}")
    
    def normalize_column_names(self):
        """Standardize column names (lowercase, underscores)"""
        self.clean_data.columns = (
            self.clean_data.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('[^a-z0-9_]', '', regex=True)
        )
        logger.info("Normalized column names")
    
    def filter_valid_percentages(self, columns):
        """
        Ensure percentage columns are between 0-100
        
        Args:
            columns: List of percentage column names
        """
        for col in columns:
            if col in self.clean_data.columns:
                invalid = ((self.clean_data[col] < 0) | (self.clean_data[col] > 100))
                invalid_count = invalid.sum()
                
                if invalid_count > 0:
                    self.clean_data = self.clean_data[~invalid]
                    logger.warning(f"Removed {invalid_count} rows with invalid percentages in '{col}'")
                    self.cleaning_report.append(f"Removed {invalid_count} invalid percentage values in '{col}'")
    
    def get_cleaned_data(self):
        """Return cleaned dataset"""
        return self.clean_data
    
    def get_cleaning_report(self):
        """Return list of cleaning actions performed"""
        return self.cleaning_report
    
    def save_cleaned_data(self, output_path):
        """
        Save cleaned data to file
        
        Args:
            output_path: Path to save cleaned data
        """
        try:
            if str(output_path).endswith('.csv'):
                self.clean_data.to_csv(output_path, index=False)
            elif str(output_path).endswith('.xlsx'):
                self.clean_data.to_excel(output_path, index=False)
            
            logger.info(f"Saved cleaned data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving cleaned data: {str(e)}")
            raise


def main():
    """Test data cleaning"""
    from data_loader import DataLoader
    
    loader = DataLoader()
    
    try:
        # Load data
        df = loader.load_itu_regional_data()
        
        # Clean data
        cleaner = DataCleaner(df)
        cleaner.normalize_column_names()
        cleaner.remove_duplicates()
        cleaner.handle_missing_values(strategy='interpolate')
        
        cleaned = cleaner.get_cleaned_data()
        
        print(f"\n✓ Data cleaning completed")
        print(f"Original shape: {df.shape}")
        print(f"Cleaned shape: {cleaned.shape}")
        print(f"\nCleaning actions performed:")
        for action in cleaner.get_cleaning_report():
            print(f"  - {action}")
        
    except Exception as e:
        print(f"\n✗ Error during cleaning: {str(e)}")


if __name__ == "__main__":
    main()
