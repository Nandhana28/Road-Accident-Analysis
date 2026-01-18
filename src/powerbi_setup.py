"""
Power BI Setup - Generates all data for Power BI visualizations
"""

import pandas as pd
import json


class PowerBISetup:
    def __init__(self, df):
        self.df = df
        
    def generate_all(self):
        """Generate all Power BI datasets"""
        print("\n[*] Generating Power BI Datasets...")
        
        # 1. KPI Summary
        kpi_data = {
            'Total Crashes': len(self.df),
            'Fatal Crashes': int(self.df['injuries_fatal'].sum()),
            'Total Injuries': int(self.df['injuries_total'].sum()),
            'Severe Injuries': int(self.df['injuries_incapacitating'].sum()),
            'Fatal Rate %': round((self.df['injuries_fatal'].sum() / len(self.df)) * 100, 2),
            'Injury Rate %': round((self.df['injuries_total'].sum() / len(self.df)) * 100, 2),
        }
        
        with open('output/powerbi_kpi.json', 'w') as f:
            json.dump(kpi_data, f, indent=2)
        
        # 2. Hourly Analysis
        hourly = self.df.groupby('crash_hour').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        hourly.to_csv('output/powerbi_hourly.csv')
        
        # 3. Daily Analysis
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = self.df.groupby('crash_day_of_week').agg({
            'crash_date': 'count',
            'injuries_total': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        daily['Day'] = [day_names[i] if i < 7 else f'Day {i}' for i in daily.index]
        daily.to_csv('output/powerbi_daily.csv')
        
        # 4. Weather Analysis
        weather = self.df.groupby('weather_condition').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        weather['InjuryRate'] = (weather['injuries_total'] / weather['Crashes'] * 100).round(2)
        weather.to_csv('output/powerbi_weather.csv')
        
        # 5. Lighting Analysis
        lighting = self.df.groupby('lighting_condition').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        lighting['InjuryRate'] = (lighting['injuries_total'] / lighting['Crashes'] * 100).round(2)
        lighting.to_csv('output/powerbi_lighting.csv')
        
        # 6. Crash Type Analysis
        crash_type = self.df.groupby('first_crash_type').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        crash_type['InjuryRate'] = (crash_type['injuries_total'] / crash_type['Crashes'] * 100).round(2)
        crash_type = crash_type.sort_values('Crashes', ascending=False)
        crash_type.to_csv('output/powerbi_crash_type.csv')
        
        # 7. Road Surface Analysis
        surface = self.df.groupby('roadway_surface_cond').agg({
            'crash_date': 'count',
            'injuries_total': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        surface['InjuryRate'] = (surface['injuries_total'] / surface['Crashes'] * 100).round(2)
        surface.to_csv('output/powerbi_surface.csv')
        
        # 8. Trafficway Type Analysis
        trafficway = self.df.groupby('trafficway_type').agg({
            'crash_date': 'count',
            'injuries_total': 'sum'
        }).rename(columns={'crash_date': 'Crashes'})
        trafficway['InjuryRate'] = (trafficway['injuries_total'] / trafficway['Crashes'] * 100).round(2)
        trafficway.to_csv('output/powerbi_trafficway.csv')
        
        print("[OK] Generated 8 Power BI datasets")
        return kpi_data
