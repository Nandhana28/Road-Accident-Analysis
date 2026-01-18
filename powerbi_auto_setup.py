"""
ONE-CLICK Power BI Setup
Run this script to auto-generate all measures and charts for Power BI
Simply copy-paste the output into Power BI
"""

import pandas as pd
import json

# Load the cleaned data
df = pd.read_csv('output/cleaned_accidents_data.csv')

print("\n" + "="*80)
print("POWER BI AUTO SETUP - GENERATING ALL MEASURES & CHARTS")
print("="*80)

# ============================================================================
# STEP 1: CREATE ALL DAX MEASURES
# ============================================================================
print("\n[STEP 1] DAX MEASURES - Copy & Paste into Power BI")
print("-" * 80)

measures = {
    "Total Crashes": "COUNTA(cleaned_accidents_data[crash_date])",
    "Fatal Crashes": "SUM(cleaned_accidents_data[injuries_fatal])",
    "Total Injuries": "SUM(cleaned_accidents_data[injuries_total])",
    "Severe Injuries": "SUM(cleaned_accidents_data[injuries_incapacitating])",
    "Fatal Rate %": "DIVIDE(SUM(cleaned_accidents_data[injuries_fatal]), COUNTA(cleaned_accidents_data[crash_date]), 0) * 100",
    "Injury Rate %": "DIVIDE(SUM(cleaned_accidents_data[injuries_total]), COUNTA(cleaned_accidents_data[crash_date]), 0) * 100",
    "Avg Units": "AVERAGE(cleaned_accidents_data[num_units])",
    "Severe Rate %": "DIVIDE(SUM(cleaned_accidents_data[injuries_incapacitating]), SUM(cleaned_accidents_data[injuries_total]), 0) * 100",
    "Crashes with Injuries": "CALCULATE(COUNTA(cleaned_accidents_data[crash_date]), cleaned_accidents_data[injuries_total] > 0)",
    "Injury-Free Crashes": "CALCULATE(COUNTA(cleaned_accidents_data[crash_date]), cleaned_accidents_data[injuries_total] = 0)",
}

print("\nCopy each measure below into Power BI (Home > New Measure):\n")
for name, formula in measures.items():
    print(f"{name} =")
    print(f"{formula}\n")

# ============================================================================
# STEP 2: CHART SPECIFICATIONS
# ============================================================================
print("\n" + "="*80)
print("[STEP 2] CHART SPECIFICATIONS - Create These Visualizations")
print("="*80)

charts = [
    {
        "name": "Total Crashes (Card)",
        "type": "Card",
        "measure": "Total Crashes",
        "color": "Blue (#1F77B4)",
        "font_size": "44pt"
    },
    {
        "name": "Fatal Crashes (Card)",
        "type": "Card",
        "measure": "Fatal Crashes",
        "color": "Red (#D62728)",
        "font_size": "44pt"
    },
    {
        "name": "Total Injuries (Card)",
        "type": "Card",
        "measure": "Total Injuries",
        "color": "Orange (#FF7F0E)",
        "font_size": "44pt"
    },
    {
        "name": "Severe Injuries (Card)",
        "type": "Card",
        "measure": "Severe Injuries",
        "color": "Purple (#9467BD)",
        "font_size": "44pt"
    },
    {
        "name": "Crashes by Hour",
        "type": "Column Chart",
        "x_axis": "crash_hour",
        "y_axis": "Count of crash_date",
        "color": "Blue gradient",
        "title": "Peak Crash Hours"
    },
    {
        "name": "Crashes by Day",
        "type": "Bar Chart",
        "x_axis": "Count of crash_date",
        "y_axis": "day_name",
        "color": "Green gradient",
        "title": "Crashes by Day of Week"
    },
    {
        "name": "Weather Distribution",
        "type": "Pie Chart",
        "values": "Count of crash_date",
        "legend": "weather_condition",
        "title": "Crashes by Weather"
    },
    {
        "name": "Crash Types",
        "type": "Donut Chart",
        "values": "Count of crash_date",
        "legend": "first_crash_type",
        "title": "Crash Type Distribution"
    },
    {
        "name": "Road Surface Impact",
        "type": "Horizontal Bar Chart",
        "x_axis": "Count of crash_date",
        "y_axis": "roadway_surface_cond",
        "color": "Orange gradient",
        "title": "Crashes by Road Surface"
    },
    {
        "name": "Lighting Conditions",
        "type": "Clustered Bar Chart",
        "x_axis": "lighting_condition",
        "y_axis": "Count of crash_date",
        "series": "injuries_fatal",
        "title": "Lighting Conditions & Fatalities"
    },
    {
        "name": "Injury Severity",
        "type": "100% Stacked Bar Chart",
        "x_axis": "crash_type",
        "y_axis": "Count of crash_date",
        "stack_by": "most_severe_injury",
        "title": "Injury Severity by Crash Type"
    },
    {
        "name": "Top Contributory Causes",
        "type": "Horizontal Bar Chart",
        "x_axis": "Count of crash_date",
        "y_axis": "prim_contributory_cause (top 10)",
        "color": "Purple gradient",
        "title": "Top 10 Contributory Causes"
    }
]

for i, chart in enumerate(charts, 1):
    print(f"\n[CHART {i}] {chart['name']}")
    print(f"  Type: {chart['type']}")
    if 'measure' in chart:
        print(f"  Measure: {chart['measure']}")
    if 'x_axis' in chart:
        print(f"  X-Axis: {chart['x_axis']}")
    if 'y_axis' in chart:
        print(f"  Y-Axis: {chart['y_axis']}")
    if 'values' in chart:
        print(f"  Values: {chart['values']}")
    if 'legend' in chart:
        print(f"  Legend: {chart['legend']}")
    if 'color' in chart:
        print(f"  Color: {chart['color']}")
    if 'title' in chart:
        print(f"  Title: {chart['title']}")

# ============================================================================
# STEP 3: CAUSAL ANALYSIS INSIGHTS
# ============================================================================
print("\n" + "="*80)
print("[STEP 3] CAUSAL ANALYSIS INSIGHTS - Add as Text Boxes")
print("="*80)

# Calculate causal insights
top_factors = df.select_dtypes(include=['number']).corr()['injuries_total'].sort_values(ascending=False).head(5)
peak_hour = df.groupby('crash_hour').size().idxmax()
peak_day = df.groupby('crash_day_of_week').size().idxmax()
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
peak_day_name = day_names[peak_day] if peak_day < 7 else f'Day {peak_day}'

insights = [
    f"Peak Crash Hour: {peak_hour}:00 with {df[df['crash_hour']==peak_hour].shape[0]:,} crashes",
    f"Peak Crash Day: {peak_day_name} with {df[df['crash_day_of_week']==peak_day].shape[0]:,} crashes",
    f"Fatal Crash Rate: {(df['injuries_fatal'].sum() / len(df) * 100):.2f}%",
    f"Injury Rate: {(df['injuries_total'].sum() / len(df) * 100):.2f}%",
    f"Most Common Crash Type: {df['first_crash_type'].value_counts().index[0]} ({df['first_crash_type'].value_counts().values[0]:,} crashes)",
    f"Most Dangerous Weather: {df.groupby('weather_condition').apply(lambda x: (x['injuries_total'] > 0).sum() / len(x) * 100).idxmax()}",
]

for i, insight in enumerate(insights, 1):
    print(f"\n[INSIGHT {i}]")
    print(f"  {insight}")

# ============================================================================
# STEP 4: IMPORT DATA SOURCES
# ============================================================================
print("\n" + "="*80)
print("[STEP 4] DATA SOURCES - Import These Files into Power BI")
print("="*80)

data_sources = [
    "output/cleaned_accidents_data.csv - Main dataset (98,890 records)",
    "output/powerbi_hourly.csv - Hourly crash patterns",
    "output/powerbi_daily.csv - Daily crash patterns",
    "output/powerbi_weather.csv - Weather impact analysis",
    "output/powerbi_lighting.csv - Lighting condition analysis",
    "output/powerbi_crash_type.csv - Crash type risk analysis",
    "output/powerbi_surface.csv - Road surface analysis",
    "output/powerbi_trafficway.csv - Trafficway type analysis",
]

for source in data_sources:
    print(f"  ✓ {source}")

# ============================================================================
# STEP 5: QUICK SETUP GUIDE
# ============================================================================
print("\n" + "="*80)
print("[STEP 5] QUICK SETUP GUIDE")
print("="*80)

setup_steps = [
    "1. Open Power BI Desktop",
    "2. Get Data > Text/CSV > Select output/cleaned_accidents_data.csv",
    "3. Click Load",
    "4. Create all measures (copy from STEP 1 above)",
    "5. Create visualizations (follow STEP 2 specifications)",
    "6. Add causal insights as text boxes (from STEP 3)",
    "7. Format with colors: Blue, Red, Orange, Green, Purple",
    "8. Save as Road_Accident_Analysis.pbix",
    "9. Publish to Power BI Service",
]

for step in setup_steps:
    print(f"  {step}")

# ============================================================================
# STEP 6: COLOR SCHEME
# ============================================================================
print("\n" + "="*80)
print("[STEP 6] COLOR SCHEME - Use These Colors")
print("="*80)

colors = {
    "Primary": "#1F77B4 (Deep Blue)",
    "Danger": "#D62728 (Vibrant Red)",
    "Warning": "#FF7F0E (Warm Orange)",
    "Success": "#2CA02C (Fresh Green)",
    "Accent": "#9467BD (Royal Purple)",
}

for color_type, color_code in colors.items():
    print(f"  {color_type}: {color_code}")

# ============================================================================
# SAVE CONFIGURATION
# ============================================================================
config = {
    "project": "Road Accident Analysis & Mobility Insights",
    "total_records": len(df),
    "measures": measures,
    "charts": charts,
    "insights": insights,
    "colors": colors,
    "data_sources": data_sources,
}

with open('output/powerbi_complete_setup.json', 'w') as f:
    json.dump(config, f, indent=2)

print("\n" + "="*80)
print("SETUP COMPLETE!")
print("="*80)
print("\nConfiguration saved to: output/powerbi_complete_setup.json")
print("\nNext Steps:")
print("  1. Copy all measures from STEP 1")
print("  2. Create charts following STEP 2")
print("  3. Add insights from STEP 3")
print("  4. Apply colors from STEP 6")
print("  5. Save and publish your dashboard!")
print("\n" + "="*80 + "\n")
