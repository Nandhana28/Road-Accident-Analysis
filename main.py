import os
import sys
from pathlib import Path

# Create output directory
os.makedirs('output', exist_ok=True)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
from eda import ExploratoryDataAnalysis
from powerbi_setup import PowerBISetup
from causal_analysis import CausalAnalysis

def main():
    """Main analysis pipeline"""
    
    # 1. Load data
    print("=" * 60)
    print("ROAD ACCIDENT ANALYSIS & MOBILITY INSIGHTS")
    print("=" * 60)
    
    loader = DataLoader('data/traffic_accidents.csv')
    df = loader.load()
    loader.get_info()
    
    # 2. Clean data
    print("\n" + "=" * 60)
    print("DATA CLEANING")
    print("=" * 60)
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean()
    
    # 3. Feature engineering
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    engineer = FeatureEngineer(df_clean)
    df_engineered = engineer.engineer()
    
    # 4. Exploratory Data Analysis
    print("\n" + "=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    eda = ExploratoryDataAnalysis(df_engineered)
    insights = eda.run_full_analysis()
    
    # 5. Power BI Setup & Configuration
    print("\n" + "=" * 60)
    print("POWER BI SETUP & CONFIGURATION")
    print("=" * 60)
    powerbi_setup = PowerBISetup(df_engineered)
    kpi_data = powerbi_setup.generate_all()
    
    # 6. Causal Analysis & Root Cause Identification
    print("\n" + "=" * 60)
    print("CAUSAL ANALYSIS & ROOT CAUSE IDENTIFICATION")
    print("=" * 60)
    causal = CausalAnalysis(df_engineered)
    causal_results = causal.run_full_analysis()
    causal.print_summary()
    
    # 5. Save cleaned data
    print("\n" + "=" * 60)
    print("SAVING OUTPUTS")
    print("=" * 60)
    df_engineered.to_csv('output/cleaned_accidents_data.csv', index=False)
    print("✓ Cleaned data saved to output/cleaned_accidents_data.csv")
    
    # 6. Save insights
    import json
    with open('output/insights_summary.json', 'w') as f:
        json.dump(insights, f, indent=2, default=str)
    print("✓ Insights saved to output/insights_summary.json")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - output/cleaned_accidents_data.csv")
    print("  - output/insights_summary.json")
    print("  - output/powerbi_config.json")
    print("  - output/causal_analysis.json")
    print("  - output/powerbi_feature_importance.csv")
    print("  - output/powerbi_interactions.csv")
    print("  - output/powerbi_crash_type_risk.csv")
    print("  - output/powerbi_temporal_risk.csv")
    print("  - output/powerbi_weather_factors.csv")
    print("  - output/powerbi_lighting_factors.csv")
    print("\n✓ All data ready for Power BI import!")

if __name__ == '__main__':
    main()
