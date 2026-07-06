# Project 3 – Log File Analyzer

A DevOps-style project that reads application logs, counts message levels, and saves a summary.

## What it does

- Reads `application.log`
- Counts `INFO`, `WARNING`, and `ERROR` messages
- Displays a summary in the console
- Saves a summary CSV to `summary.csv`
- Saves only error entries to `errors.txt`
- Finds the most frequent error message
- Supports filtering by date via the code

## Files

- `main.py` - log analyzer script
- `application.log` - sample log file
- `summary.csv` - generated summary report
- `errors.txt` - extracted error entries
- `README.md` - project documentation

## Usage

```bash
python main.py
```

## Notes

- The script parses log lines in the format `YYYY-MM-DD HH:MM:SS LEVEL message`.
- Add your own `application.log` content and rerun `main.py`.
