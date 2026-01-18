import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
    
    def clean(self):
        """Main cleaning pipeline"""
        print("Starting data cleaning...")
        
        # Handle missing values
        self._handle_missing_values()
        
        # Handle UNKNOWN values
        self._handle_unknown_values()
        
        # Data type conversions
        self._convert_types()
        
        # Remove duplicates
        self._remove_duplicates()
        
        print(f"Cleaning complete. Final shape: {self.df.shape}")
        return self.df
    
    def _handle_missing_values(self):
        """Fill or drop missing values strategically"""
        print("Handling missing values...")
        
        # For numeric columns, fill with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # For categorical columns, fill with 'Unknown'
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna('Unknown', inplace=True)
    
    def _handle_unknown_values(self):
        """Replace UNKNOWN/Unknown/unknown with standardized Unknown"""
        print("Standardizing UNKNOWN values...")
        
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].replace(
                ['UNKNOWN', 'Unknown', 'unknown', 'N/A', 'n/a'],
                'Unknown'
            )
    
    def _convert_types(self):
        """Convert columns to appropriate data types"""
        print("Converting data types...")
        
        # Convert time-based fields if they exist
        time_cols = ['crash_hour', 'crash_day_of_week', 'crash_month']
        for col in time_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
    
    def _remove_duplicates(self):
        """Remove duplicate rows"""
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed = initial_rows - len(self.df)
        if removed > 0:
            print(f"Removed {removed} duplicate rows")
