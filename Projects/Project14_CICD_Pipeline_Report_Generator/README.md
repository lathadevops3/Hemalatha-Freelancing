# CI/CD Pipeline Report Generator

Generate Excel-based reports from pipeline run data (simulated demo data provided).

**Features**
- Create sample CI/CD run data
- Generate `cicd_report.xlsx` with summaries and charts

**Demo screenshot**: `screenshots/screenshot.png`
**Demo GIF**: `screenshots/demo.gif`

## Setup
```
pip install -r requirements.txt
```

## Run (demo)
```
python main.py --demo
```
# Project 14 – CI/CD Pipeline Report Generator

Parses CI pipeline run JSON and creates an Excel report with runs, summary, and timing metrics.

Files
- `main.py` - generates a sample `sample_ci_runs.json` and writes `cicd_report.xlsx`
- `requirements.txt` - `pandas`, `openpyxl`
- `screenshots/` - placeholder folder

Usage

```bash
python main.py
```

## Screenshots

![CI/CD Pipeline Report Generator](screenshots/screenshot.png)

