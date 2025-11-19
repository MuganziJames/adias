"""
Data Ingestion Module
Loads and parses ITU Excel datasets
"""
import pandas as pd
import logging
from pathlib import Path
import config

# Setup logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading of ITU datasets"""
    
    def __init__(self):
        self.regional_data = None
        self.gender_data = None
        
    def load_itu_regional_data(self, file_path=None):
        """
        Load ITU regional/global ICT indicators
        
        Args:
            file_path: Path to ITU Excel file. Defaults to config path.
            
        Returns:
            pd.DataFrame: Loaded and parsed data
        """
        if file_path is None:
            file_path = config.ITU_REGIONAL_FILE
            
        try:
            logger.info(f"Loading ITU regional data from {file_path}")
            
            # ITU files typically have multiple sheets
            # Try to load the main data sheet
            xls = pd.ExcelFile(file_path)
            logger.info(f"Available sheets: {xls.sheet_names}")
            
            # Load the first data sheet (usually contains main indicators)
            # Adjust sheet_name based on actual file structure
            df = pd.read_excel(file_path, sheet_name=0)
            
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            logger.info(f"Columns: {df.columns.tolist()}")
            
            self.regional_data = df
            return df
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading ITU regional data: {str(e)}")
            raise
    
    def load_itu_gender_data(self, file_path=None):
        """
        Load ITU gender ICT statistics
        
        Args:
            file_path: Path to ITU gender Excel file
            
        Returns:
            pd.DataFrame: Loaded gender data
        """
        if file_path is None:
            file_path = config.ITU_GENDER_FILE
            
        try:
            logger.info(f"Loading ITU gender data from {file_path}")
            
            xls = pd.ExcelFile(file_path)
            logger.info(f"Available sheets: {xls.sheet_names}")
            
            df = pd.read_excel(file_path, sheet_name=0)
            
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            
            self.gender_data = df
            return df
            
        except FileNotFoundError:
            logger.warning(f"Gender data file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading ITU gender data: {str(e)}")
            return None
    
    def get_available_indicators(self):
        """
        Extract list of available indicators from loaded data
        
        Returns:
            list: Available indicator names
        """
        if self.regional_data is None:
            logger.warning("No data loaded yet")
            return []
        
        # Return column names (indicators)
        return self.regional_data.columns.tolist()
    
    def get_data_summary(self):
        """
        Get summary information about loaded data
        
        Returns:
            dict: Summary statistics
        """
        summary = {}
        
        if self.regional_data is not None:
            summary['regional'] = {
                'rows': len(self.regional_data),
                'columns': len(self.regional_data.columns),
                'indicators': self.regional_data.columns.tolist(),
                'missing_values': self.regional_data.isnull().sum().to_dict()
            }
        
        if self.gender_data is not None:
            summary['gender'] = {
                'rows': len(self.gender_data),
                'columns': len(self.gender_data.columns)
            }
        
        return summary


def main():
    """Test data loading"""
    loader = DataLoader()
    
    # Try to load data
    try:
        df = loader.load_itu_regional_data()
        print(f"\n✓ Successfully loaded ITU regional data")
        print(f"Shape: {df.shape}")
        print(f"\nFirst few rows:\n{df.head()}")
        print(f"\nData summary:\n{loader.get_data_summary()}")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nPlease ensure ITU data files are placed in the data/ folder:")
        print(f"  - {config.ITU_REGIONAL_FILE}")
        print(f"  - {config.ITU_GENDER_FILE}")


if __name__ == "__main__":
    main()
