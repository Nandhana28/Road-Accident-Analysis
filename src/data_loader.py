import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
    
    def load(self):
        """Load CSV data"""
        self.df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self.df
    
    def get_info(self):
        """Display dataset info"""
        print("\n=== Dataset Info ===")
        print(self.df.info())
        print("\n=== First Few Rows ===")
        print(self.df.head())
        print("\n=== Missing Values ===")
        print(self.df.isnull().sum())
