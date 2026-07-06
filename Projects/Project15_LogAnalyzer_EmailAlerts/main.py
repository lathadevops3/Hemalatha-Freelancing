from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import smtplib
from email.message import EmailMessage

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "application.log"
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
    if not path.exists():
        # create a small sample log
        path.write_text(
            "2026-07-04 10:00:01 INFO Service started\n2026-07-04 10:01:20 ERROR Database connection failed\n",
            encoding="utf-8",
        )
    raw = path.read_text(encoding="utf-8")
    entries = []
    for line in raw.splitlines():
        parsed = parse_log_line(line)
        if parsed:
            entries.append(parsed)
    return entries


def write_errors(path: Path, entries: List[LogEntry]):
    errors = [f"{e.timestamp} {e.level} {e.message}" for e in entries if e.level == "ERROR"]
    path.write_text("\n".join(errors), encoding="utf-8")


def send_alert(subject: str, body: str, recipients: List[str]):
    # Placeholder email send - prints the message and writes to a file for demo
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "alerts@example.com"
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)
    out = BASE_DIR / "last_alert.eml"
    out.write_text(msg.as_string(), encoding="utf-8")
    print(f"Wrote alert to {out}")


def demo():
    print("Log Analyzer + Email Alerts Demo")
    entries = load_log_file(LOG_FILE)
    write_errors(ERROR_FILE, entries)
    error_count = sum(1 for e in entries if e.level == "ERROR")
    print(f"Found {error_count} errors")
    if error_count:
        send_alert("Automated Log Alert", f"Found {error_count} errors in logs.", ["admin@example.com"])


if __name__ == "__main__":
    demo()
