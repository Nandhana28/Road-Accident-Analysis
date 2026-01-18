import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
    
    def engineer(self):
        """Create new features for analysis"""
        print("Engineering features...")
        
        # Time-based features
        self._create_time_features()
        
        # Risk categorization
        self._create_risk_categories()
        
        # Condition-based features
        self._create_condition_features()
        
        print(f"Feature engineering complete. New shape: {self.df.shape}")
        return self.df
    
    def _create_time_features(self):
        """Create time-based feature categories"""
        if 'crash_hour' in self.df.columns:
            self.df['hour_category'] = pd.cut(
                self.df['crash_hour'],
                bins=[0, 6, 12, 18, 24],
                labels=['Night (0-6)', 'Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-24)'],
                include_lowest=True
            )
        
        if 'crash_day_of_week' in self.df.columns:
            day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                      4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
            self.df['day_name'] = self.df['crash_day_of_week'].map(day_map)
            
            # Weekday vs Weekend
            self.df['is_weekend'] = self.df['crash_day_of_week'].isin([5, 6])
    
    def _create_risk_categories(self):
        """Categorize crashes by severity"""
        if 'injury_severity' in self.df.columns:
            severity_map = {
                'Fatal': 'Fatal',
                'Serious Injury': 'Serious',
                'Other Injury': 'Other',
                'Non-Injury': 'Non-Injury',
                'Unknown': 'Unknown'
            }
            self.df['severity_category'] = self.df['injury_severity'].map(severity_map)
            self.df['severity_category'].fillna('Unknown', inplace=True)
            
            # Binary: Severe (Fatal/Serious) vs Non-Severe
            self.df['is_severe'] = self.df['severity_category'].isin(['Fatal', 'Serious']).astype(int)
    
    def _create_condition_features(self):
        """Create condition-based features"""
        # These will depend on actual column names in your dataset
        # Adjust based on your CSV structure
        pass
