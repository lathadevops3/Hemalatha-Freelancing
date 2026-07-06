# File Watcher → WebSocket Notifier (RT04)

Watch a folder for changes and notify connected WebSocket clients. Demo mode prints a sample event and creates `screenshots/screenshot.png`.

## Setup
```
pip install -r requirements.txt
```

## Run (demo)
```
python main.py --demo
```
# RT04 — File-change Watcher with WebSocket Notifications

Watches a directory and broadcasts create events over WebSocket.

Demo (writes sample files into `watch_dir`):

```bash
python main.py --demo
```

Requirements:

```bash
pip install watchdog websockets
```

Screenshots: `screenshots/screenshot.png`
