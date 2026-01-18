import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ExploratoryDataAnalysis:
    def __init__(self, df):
        self.df = df
        self.insights = {}
    
    def run_full_analysis(self):
        """Run complete EDA"""
        print("Starting Exploratory Data Analysis...")
        
        self._temporal_analysis()
        self._condition_analysis()
        self._severity_analysis()
        self._road_analysis()
        self._generate_summary()
        
        return self.insights
    
    def _temporal_analysis(self):
        """Analyze temporal patterns"""
        print("\n=== Temporal Analysis ===")
        
        if 'crash_hour' in self.df.columns:
            hourly_crashes = self.df['crash_hour'].value_counts().sort_index()
            print(f"Peak crash hour: {hourly_crashes.idxmax()} with {hourly_crashes.max()} crashes")
            self.insights['peak_hour'] = hourly_crashes.idxmax()
            
            # Visualization
            fig = px.bar(
                x=hourly_crashes.index,
                y=hourly_crashes.values,
                title='Crashes by Hour of Day',
                labels={'x': 'Hour', 'y': 'Number of Crashes'}
            )
            fig.write_html('output/crashes_by_hour.html')
        
        if 'crash_day_of_week' in self.df.columns:
            daily_crashes = self.df['crash_day_of_week'].value_counts().sort_index()
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_labels = [day_names[int(i)] if int(i) < len(day_names) else f'Day {i}' for i in daily_crashes.index]
            print(f"Crashes by day: {dict(zip(day_labels, daily_crashes.values))}")
            
            fig = px.bar(
                x=day_labels,
                y=daily_crashes.values,
                title='Crashes by Day of Week',
                labels={'x': 'Day', 'y': 'Number of Crashes'}
            )
            fig.write_html('output/crashes_by_day.html')
        
        if 'crash_month' in self.df.columns:
            monthly_crashes = self.df['crash_month'].value_counts().sort_index()
            print(f"Peak crash month: {monthly_crashes.idxmax()} with {monthly_crashes.max()} crashes")
            self.insights['peak_month'] = monthly_crashes.idxmax()
    
    def _condition_analysis(self):
        """Analyze weather and road conditions"""
        print("\n=== Condition Analysis ===")
        
        condition_cols = [col for col in self.df.columns if 'weather' in col.lower() or 'condition' in col.lower()]
        
        for col in condition_cols:
            if col in self.df.columns:
                condition_counts = self.df[col].value_counts()
                print(f"\n{col}:")
                print(condition_counts.head())
                
                fig = px.bar(
                    x=condition_counts.index[:10],
                    y=condition_counts.values[:10],
                    title=f'Top 10 {col}',
                    labels={'x': col, 'y': 'Count'}
                )
                fig.write_html(f'output/{col}_distribution.html')
    
    def _severity_analysis(self):
        """Analyze injury severity patterns"""
        print("\n=== Severity Analysis ===")
        
        if 'injury_severity' in self.df.columns:
            severity_counts = self.df['injury_severity'].value_counts()
            print(severity_counts)
            self.insights['severity_distribution'] = severity_counts.to_dict()
            
            # Pie chart
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title='Crash Severity Distribution'
            )
            fig.write_html('output/severity_distribution.html')
            
            # Fatal crashes analysis
            fatal_count = (self.df['injury_severity'] == 'Fatal').sum()
            total_crashes = len(self.df)
            fatal_rate = (fatal_count / total_crashes) * 100
            print(f"\nFatal crashes: {fatal_count} ({fatal_rate:.2f}%)")
            self.insights['fatal_crashes'] = fatal_count
            self.insights['fatal_rate'] = fatal_rate
    
    def _road_analysis(self):
        """Analyze road-related factors"""
        print("\n=== Road Analysis ===")
        
        road_cols = [col for col in self.df.columns if 'road' in col.lower() or 'type' in col.lower()]
        
        for col in road_cols:
            if col in self.df.columns:
                road_counts = self.df[col].value_counts()
                print(f"\n{col}:")
                print(road_counts.head())
    
    def _generate_summary(self):
        """Generate summary statistics"""
        print("\n=== Summary Statistics ===")
        print(f"Total crashes analyzed: {len(self.df)}")
        print(f"Dataset shape: {self.df.shape}")
        print(f"Date range: Analysis period")
        
        self.insights['total_crashes'] = len(self.df)
        self.insights['total_columns'] = len(self.df.columns)
