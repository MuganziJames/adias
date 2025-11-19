"""
Sample Data Generator
Creates synthetic digital inequality data for testing when real ITU data is not available
"""
import pandas as pd
import numpy as np
from pathlib import Path
import config

np.random.seed(42)

def generate_sample_data():
    """Generate realistic sample data for digital inequality analysis"""
    
    # Define regions
    regions = [
        'North America', 'Western Europe', 'Eastern Europe', 'East Asia',
        'Southeast Asia', 'South Asia', 'Middle East', 'North Africa',
        'Sub-Saharan Africa', 'Latin America', 'Caribbean', 'Oceania',
        'Central Asia', 'Southern Africa', 'West Africa', 'East Africa',
        'Central America', 'Nordic Countries', 'Baltic States', 'Balkans'
    ]
    
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    
    data = []
    
    for region in regions:
        for year in years:
            # Base internet access with regional variations
            base_access = {
                'North America': 90, 'Western Europe': 88, 'Eastern Europe': 75,
                'East Asia': 85, 'Southeast Asia': 65, 'South Asia': 45,
                'Middle East': 70, 'North Africa': 55, 'Sub-Saharan Africa': 30,
                'Latin America': 68, 'Caribbean': 60, 'Oceania': 82,
                'Central Asia': 58, 'Southern Africa': 52, 'West Africa': 35,
                'East Africa': 28, 'Central America': 62, 'Nordic Countries': 95,
                'Baltic States': 85, 'Balkans': 72
            }
            
            # Trend improvement over years
            year_multiplier = 1 + (year - 2020) * 0.03
            
            internet_access = min(98, base_access.get(region, 50) * year_multiplier)
            internet_access += np.random.normal(0, 3)  # Add some variation
            
            # Rural is typically 20-40% less than overall
            rural_access = max(5, internet_access - np.random.uniform(20, 40))
            
            # Urban is typically 10-20% more than overall
            urban_access = min(99, internet_access + np.random.uniform(10, 20))
            
            # Mobile coverage is generally higher
            mobile_coverage = min(99, internet_access + np.random.uniform(5, 15))
            
            # Device ownership correlates with internet access
            device_ownership = internet_access * np.random.uniform(0.7, 0.9)
            
            # Digital literacy correlates with access but lower
            digital_literacy = internet_access * np.random.uniform(0.6, 0.8)
            
            # Population (millions)
            population = np.random.uniform(10, 500)
            
            data.append({
                'Region': region,
                'Year': year,
                'Internet_Access_Percentage': round(internet_access, 2),
                'Rural_Internet_Access': round(rural_access, 2),
                'Urban_Internet_Access': round(urban_access, 2),
                'Mobile_Network_Coverage': round(mobile_coverage, 2),
                'Device_Ownership_Index': round(device_ownership, 2),
                'Digital_Literacy_Score': round(digital_literacy, 2),
                'Population_Millions': round(population, 2),
                'Broadband_Subscriptions_Per_100': round(internet_access * 0.6, 2),
                'Mobile_Subscriptions_Per_100': round(mobile_coverage * 1.2, 2)
            })
    
    df = pd.DataFrame(data)
    return df


def save_sample_data():
    """Generate and save sample data to the data folder"""
    print("\n" + "="*60)
    print("ADIAS Sample Data Generator")
    print("="*60 + "\n")
    
    print("Generating synthetic digital inequality data...")
    df = generate_sample_data()
    
    # Save to data folder
    output_path = config.DATA_DIR / 'sample_digital_inequality_data.xlsx'
    df.to_excel(output_path, index=False, sheet_name='Digital_Inequality_Data')
    
    print(f"✓ Generated {len(df)} records")
    print(f"✓ Data saved to: {output_path}")
    print(f"\nData summary:")
    print(f"  - Regions: {df['Region'].nunique()}")
    print(f"  - Years: {df['Year'].min()} - {df['Year'].max()}")
    print(f"  - Avg Internet Access: {df['Internet_Access_Percentage'].mean():.1f}%")
    print(f"  - Min Internet Access: {df['Internet_Access_Percentage'].min():.1f}%")
    print(f"  - Max Internet Access: {df['Internet_Access_Percentage'].max():.1f}%")
    
    print(f"\n✓ Sample data ready for testing!")
    print(f"\nTo use this data, update config.py:")
    print(f"  ITU_REGIONAL_FILE = DATA_DIR / 'sample_digital_inequality_data.xlsx'")
    
    return output_path


if __name__ == "__main__":
    save_sample_data()
