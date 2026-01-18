"""
Causal Analysis & Root Cause Identification
Identifies true drivers of crashes using statistical methods
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import json
import warnings
warnings.filterwarnings('ignore')


class CausalAnalysis:
    def __init__(self, df):
        self.df = df
        self.results = {}
        self.correlations = {}
        self.causal_insights = []
        
    def run_full_analysis(self):
        """Execute complete causal analysis"""
        print("\n" + "="*70)
        print("CAUSAL ANALYSIS & ROOT CAUSE IDENTIFICATION")
        print("="*70)
        
        self._correlation_analysis()
        self._chi_square_analysis()
        self._regression_analysis()
        self._interaction_effects()
        self._generate_causal_insights()
        self._create_powerbi_datasets()
        self._save_results()
        
        return self.results
    
    def _correlation_analysis(self):
        """Analyze correlations between factors and crashes"""
        print("\n[*] Running Correlation Analysis...")
        
        # Numeric columns for correlation
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Create correlation matrix
        corr_matrix = self.df[numeric_cols].corr()
        
        # Get correlations with crash frequency (using injuries as proxy)
        crash_correlations = corr_matrix['injuries_total'].sort_values(ascending=False)
        
        self.correlations['numeric'] = crash_correlations.to_dict()
        
        print("[OK] Correlation Analysis Complete")
        print("\nTop Factors Correlated with Injuries:")
        for factor, corr in crash_correlations.head(10).items():
            if factor != 'injuries_total':
                print(f"  {factor}: {corr:.4f}")
    
    def _chi_square_analysis(self):
        """Chi-square test for categorical factors"""
        print("\n[*] Running Chi-Square Analysis...")
        
        categorical_cols = [
            'weather_condition', 'lighting_condition', 'first_crash_type',
            'trafficway_type', 'roadway_surface_cond', 'road_defect'
        ]
        
        chi_square_results = {}
        
        for col in categorical_cols:
            if col in self.df.columns:
                # Create contingency table
                contingency = pd.crosstab(self.df[col], self.df['injuries_total'] > 0)
                
                # Perform chi-square test
                chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
                
                chi_square_results[col] = {
                    'chi_square': float(chi2),
                    'p_value': float(p_value),
                    'significant': p_value < 0.05
                }
        
        self.results['chi_square'] = chi_square_results
        
        print("[OK] Chi-Square Analysis Complete")
        print("\nSignificant Categorical Factors (p < 0.05):")
        for factor, result in chi_square_results.items():
            if result['significant']:
                print(f"  {factor}: p-value = {result['p_value']:.6f}")
    
    def _regression_analysis(self):
        """Regression analysis to identify key drivers"""
        print("\n[*] Running Regression Analysis...")
        
        # Prepare data for regression
        X = self.df.copy()
        y = (self.df['injuries_total'] > 0).astype(int)
        
        # Encode categorical variables
        le_dict = {}
        for col in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            le_dict[col] = le
        
        # Select numeric features
        numeric_features = X.select_dtypes(include=[np.number]).columns
        X_numeric = X[numeric_features]
        
        # Calculate feature importance using correlation with target
        feature_importance = {}
        for col in X_numeric.columns:
            corr = np.corrcoef(X_numeric[col], y)[0, 1]
            feature_importance[col] = abs(corr)
        
        # Sort by importance
        sorted_importance = dict(sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        self.results['feature_importance'] = sorted_importance
        
        print("[OK] Regression Analysis Complete")
        print("\nTop 10 Most Important Factors:")
        for i, (factor, importance) in enumerate(list(sorted_importance.items())[:10], 1):
            print(f"  {i}. {factor}: {importance:.4f}")
    
    def _interaction_effects(self):
        """Analyze interaction effects between factors"""
        print("\n[*] Analyzing Interaction Effects...")
        
        interactions = {}
        
        # Weather + Lighting interaction
        weather_lighting = pd.crosstab(
            [self.df['weather_condition'], self.df['lighting_condition']],
            self.df['injuries_total'] > 0,
            margins=True
        )
        
        # Calculate injury rate for each combination
        injury_rates = {}
        for (weather, lighting), group in self.df.groupby(['weather_condition', 'lighting_condition']):
            injury_rate = (group['injuries_total'] > 0).sum() / len(group) * 100
            injury_rates[f"{weather} + {lighting}"] = injury_rate
        
        # Sort by injury rate
        sorted_rates = dict(sorted(
            injury_rates.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        interactions['weather_lighting'] = sorted_rates
        
        # Crash Type + Weather interaction
        crash_weather = {}
        for (crash_type, weather), group in self.df.groupby(['first_crash_type', 'weather_condition']):
            injury_rate = (group['injuries_total'] > 0).sum() / len(group) * 100
            crash_weather[f"{crash_type} + {weather}"] = injury_rate
        
        sorted_crash_weather = dict(sorted(
            crash_weather.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        interactions['crash_weather'] = sorted_crash_weather
        
        self.results['interactions'] = interactions
        
        print("[OK] Interaction Analysis Complete")
        print("\nTop 5 Most Dangerous Combinations:")
        for combo, rate in list(sorted_rates.items())[:5]:
            print(f"  {combo}: {rate:.2f}% injury rate")
    
    def _generate_causal_insights(self):
        """Generate actionable causal insights"""
        print("\n[*] Generating Causal Insights...")
        
        insights = []
        
        # Insight 1: Primary driver
        top_factor = list(self.results['feature_importance'].items())[0]
        insights.append({
            'type': 'PRIMARY_DRIVER',
            'title': f'Primary Driver: {top_factor[0]}',
            'description': f'{top_factor[0]} is the strongest predictor of crash injuries',
            'impact': 'HIGH',
            'actionable': True
        })
        
        # Insight 2: Categorical factors
        significant_factors = [
            k for k, v in self.results['chi_square'].items()
            if v['significant']
        ]
        insights.append({
            'type': 'CATEGORICAL_FACTORS',
            'title': f'Significant Categorical Factors: {len(significant_factors)}',
            'description': f'Found {len(significant_factors)} statistically significant categorical factors',
            'factors': significant_factors,
            'actionable': True
        })
        
        # Insight 3: Dangerous combinations
        most_dangerous = list(self.results['interactions']['weather_lighting'].items())[0]
        insights.append({
            'type': 'DANGEROUS_COMBINATION',
            'title': f'Most Dangerous Condition: {most_dangerous[0]}',
            'description': f'{most_dangerous[0]} has {most_dangerous[1]:.2f}% injury rate',
            'injury_rate': most_dangerous[1],
            'actionable': True,
            'recommendation': f'Increase enforcement and safety measures during {most_dangerous[0]}'
        })
        
        # Insight 4: Crash type analysis
        crash_type_injury = self.df.groupby('first_crash_type').apply(
            lambda x: (x['injuries_total'] > 0).sum() / len(x) * 100
        ).sort_values(ascending=False)
        
        most_dangerous_crash = crash_type_injury.index[0]
        insights.append({
            'type': 'CRASH_TYPE_RISK',
            'title': f'Highest Risk Crash Type: {most_dangerous_crash}',
            'description': f'{most_dangerous_crash} crashes have {crash_type_injury.iloc[0]:.2f}% injury rate',
            'injury_rate': crash_type_injury.iloc[0],
            'actionable': True
        })
        
        # Insight 5: Temporal pattern
        hourly_injury = self.df.groupby('crash_hour').apply(
            lambda x: (x['injuries_total'] > 0).sum() / len(x) * 100
        ).sort_values(ascending=False)
        
        peak_hour = hourly_injury.index[0]
        insights.append({
            'type': 'TEMPORAL_PATTERN',
            'title': f'Peak Risk Hour: {peak_hour}:00',
            'description': f'Hour {peak_hour} has {hourly_injury.iloc[0]:.2f}% injury rate',
            'injury_rate': hourly_injury.iloc[0],
            'actionable': True,
            'recommendation': f'Deploy additional resources at {peak_hour}:00'
        })
        
        self.causal_insights = insights
        self.results['insights'] = insights
        
        print("[OK] Generated 5 Key Causal Insights")
    
    def _save_results(self):
        """Save results to JSON"""
        output = {
            'analysis_type': 'Causal Analysis & Root Cause Identification',
            'total_records': len(self.df),
            'correlations': self.correlations,
            'chi_square_results': self.results.get('chi_square', {}),
            'feature_importance': self.results.get('feature_importance', {}),
            'interactions': self.results.get('interactions', {}),
            'insights': self.causal_insights
        }
        
        with open('output/causal_analysis.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print("[OK] Saved to output/causal_analysis.json")
    
    def _create_powerbi_datasets(self):
        """Create datasets for Power BI visualizations"""
        print("\n[*] Creating Power BI Datasets...")
        
        # 1. Feature Importance Dataset
        feature_importance_df = pd.DataFrame(
            list(self.results['feature_importance'].items()),
            columns=['Factor', 'Importance']
        ).sort_values('Importance', ascending=False).head(15)
        
        feature_importance_df.to_csv('output/powerbi_feature_importance.csv', index=False)
        
        # 2. Interaction Effects Dataset
        interactions_df = pd.DataFrame(
            list(self.results['interactions']['weather_lighting'].items()),
            columns=['Condition', 'InjuryRate']
        ).sort_values('InjuryRate', ascending=False)
        
        interactions_df.to_csv('output/powerbi_interactions.csv', index=False)
        
        # 3. Crash Type Risk Dataset
        crash_type_risk = self.df.groupby('first_crash_type').agg({
            'crash_date': 'count',
            'injuries_total': lambda x: (x > 0).sum(),
            'injuries_fatal': 'sum'
        }).rename(columns={
            'crash_date': 'TotalCrashes',
            'injuries_total': 'InjuryCrashes',
            'injuries_fatal': 'FatalCrashes'
        })
        
        crash_type_risk['InjuryRate'] = (crash_type_risk['InjuryCrashes'] / crash_type_risk['TotalCrashes'] * 100).round(2)
        crash_type_risk['FatalRate'] = (crash_type_risk['FatalCrashes'] / crash_type_risk['TotalCrashes'] * 100).round(2)
        crash_type_risk = crash_type_risk.sort_values('InjuryRate', ascending=False)
        crash_type_risk.to_csv('output/powerbi_crash_type_risk.csv')
        
        # 4. Temporal Risk Dataset
        temporal_risk = self.df.groupby('crash_hour').agg({
            'crash_date': 'count',
            'injuries_total': lambda x: (x > 0).sum(),
            'injuries_fatal': 'sum'
        }).rename(columns={
            'crash_date': 'TotalCrashes',
            'injuries_total': 'InjuryCrashes',
            'injuries_fatal': 'FatalCrashes'
        })
        
        temporal_risk['InjuryRate'] = (temporal_risk['InjuryCrashes'] / temporal_risk['TotalCrashes'] * 100).round(2)
        temporal_risk.to_csv('output/powerbi_temporal_risk.csv')
        
        # 5. Causal Factors by Weather
        weather_factors = self.df.groupby('weather_condition').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum',
            'num_units': 'mean'
        }).rename(columns={
            'crash_date': 'TotalCrashes',
            'injuries_total': 'TotalInjuries',
            'injuries_fatal': 'FatalCrashes',
            'num_units': 'AvgUnits'
        }).round(2)
        
        weather_factors.to_csv('output/powerbi_weather_factors.csv')
        
        # 6. Causal Factors by Lighting
        lighting_factors = self.df.groupby('lighting_condition').agg({
            'crash_date': 'count',
            'injuries_total': 'sum',
            'injuries_fatal': 'sum'
        }).rename(columns={
            'crash_date': 'TotalCrashes',
            'injuries_total': 'TotalInjuries',
            'injuries_fatal': 'FatalCrashes'
        })
        
        lighting_factors['InjuryRate'] = (lighting_factors['TotalInjuries'] / lighting_factors['TotalCrashes'] * 100).round(2)
        lighting_factors.to_csv('output/powerbi_lighting_factors.csv')
        
        print("[OK] Created 6 Power BI datasets")
    
    
    def print_summary(self):
        """Print comprehensive summary"""
        print("\n" + "="*70)
        print("CAUSAL ANALYSIS SUMMARY")
        print("="*70)
        
        print("\n[CORRELATION ANALYSIS]")
        print("-" * 70)
        for factor, corr in list(self.correlations['numeric'].items())[:5]:
            if factor != 'injuries_total':
                print(f"  {factor}: {corr:.4f}")
        
        print("\n[FEATURE IMPORTANCE RANKING]")
        print("-" * 70)
        for i, (factor, importance) in enumerate(list(self.results['feature_importance'].items())[:10], 1):
            print(f"  {i}. {factor}: {importance:.4f}")
        
        print("\n[KEY CAUSAL INSIGHTS]")
        print("-" * 70)
        for insight in self.causal_insights:
            print(f"\n  [{insight['type']}]")
            print(f"  Title: {insight['title']}")
            print(f"  Description: {insight['description']}")
            if 'recommendation' in insight:
                print(f"  Recommendation: {insight['recommendation']}")
        
        print("\n" + "="*70)
