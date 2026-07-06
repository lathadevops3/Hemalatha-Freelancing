from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "application.log"
SUMMARY_FILE = BASE_DIR / "summary.csv"
ERROR_FILE = BASE_DIR / "errors.txt"

LOG_LEVELS = ["INFO", "WARNING", "ERROR"]


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str


def parse_log_line(line: str) -> Optional[LogEntry]:
    line = line.strip()
    if not line:
        return None

    for level in LOG_LEVELS:
        if f" {level} " in line:
            parts = line.split(f" {level} ", maxsplit=1)
            if len(parts) != 2:
                return None
            timestamp_str, message = parts
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                return LogEntry(timestamp=timestamp, level=level, message=message.strip())
            except ValueError:
                return None
    return None


def load_log_file(path: Path) -> List[LogEntry]:
    raw_text = path.read_text(encoding="utf-8")
    lines = [line for line in raw_text.replace("\r", "").split("\n") if line]
    entries = []
    for raw_line in lines:
        parts = []
        start = 0
        for level in LOG_LEVELS:
            pos = raw_line.find(f" {level} ", start)
            if pos != -1:
                parts.append((pos, level))
        if not parts:
            continue
        parts.sort()
        cursor = 0
        for i, (_, level) in enumerate(parts):
            next_start = parts[i + 1][0] if i + 1 < len(parts) else len(raw_line)
            segment = raw_line[cursor:next_start].strip()
            parsed = parse_log_line(segment)
            if parsed:
                entries.append(parsed)
            cursor = next_start
    return entries


def summarize(entries: List[LogEntry]) -> Counter:
    return Counter(entry.level for entry in entries)


def save_summary(path: Path, summary: Counter) -> None:
    lines = ["Level,Count"]
    for level in LOG_LEVELS:
        lines.append(f"{level},{summary.get(level, 0)}")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_errors(path: Path, entries: List[LogEntry]) -> None:
    error_lines = [f"{entry.timestamp} {entry.level} {entry.message}" for entry in entries if entry.level == "ERROR"]
    path.write_text("\n".join(error_lines), encoding="utf-8")


def most_frequent_error(entries: List[LogEntry]) -> Optional[str]:
    errors = [entry.message for entry in entries if entry.level == "ERROR"]
    if not errors:
        return None
    return Counter(errors).most_common(1)[0][0]


def filter_by_date(entries: List[LogEntry], date_str: str) -> List[LogEntry]:
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return [entry for entry in entries if entry.timestamp.date() == target_date]


def main() -> None:
    print("Log File Analyzer")
    print(f"Reading log file: {LOG_FILE}")
    entries = load_log_file(LOG_FILE)
    summary = summarize(entries)

    print("Summary:")
    for level in LOG_LEVELS:
        print(f"  {level}: {summary.get(level, 0)}")

    save_summary(SUMMARY_FILE, summary)
    write_errors(ERROR_FILE, entries)

    most_error = most_frequent_error(entries)
    if most_error:
        print(f"Most frequent error: {most_error}")
    else:
        print("No errors found.")

    print(f"Summary saved to: {SUMMARY_FILE}")
    print(f"Error entries saved to: {ERROR_FILE}")


if __name__ == "__main__":
    main()
