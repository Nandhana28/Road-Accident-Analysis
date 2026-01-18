# Road Accident Analysis & Mobility Insights

Comprehensive analysis of traffic accident data with 90,000+ rows to extract actionable mobility insights.

## Project Structure

```
├── data/
│   └── traffic_accidents.csv          # Raw dataset (90,000+ rows)
├── src/
│   ├── data_loader.py                 # Load CSV data
│   ├── data_cleaner.py                # Clean & handle missing values
│   ├── feature_engineer.py            # Create new features
│   └── eda.py                         # Exploratory Data Analysis
├── output/                            # Generated outputs
├── main.py                            # Main analysis pipeline
└── requirements.txt                   # Dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

## Run Analysis

```bash
python main.py
```

## Outputs

- `cleaned_accidents_data.csv` - Cleaned dataset ready for Power BI
- `insights_summary.json` - Key metrics and findings
- `*.html` - Interactive Plotly visualizations

## Key Insights Generated

- Peak crash hours and days
- Severity distribution (Fatal, Serious, Other, Non-Injury)
- Weather and road condition patterns
- High-risk factors and temporal trends
