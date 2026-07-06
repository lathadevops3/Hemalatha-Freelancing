# Excel Sales Report Generator

This project reads multiple sales Excel files and generates a unified summary report with:

- Total sales
- Average sales
- Highest sale
- Lowest sale
- Sales by region
- Sales by product
- Monthly sales totals

The program also saves the summary to `output.xlsx`.

## Files

- `main.py` - the Python script that reads all `.xlsx` files found in `inputs/`, calculates the report, and writes `output.xlsx`
- `inputs/` - folder containing sample sales input files
- `output.xlsx` - generated summary report
- `README.md` - project documentation
- `requirements.txt` - required Python packages

## Input file requirements

Each input workbook must contain the following columns:

- `Name`
- `Sales`
- `Region`
- `Date`
- `Product`

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add or update Excel files in `inputs/`.

3. Run the report generator:

```bash
python main.py
```

4. Open `output.xlsx` to view the summary and detailed worksheets.
