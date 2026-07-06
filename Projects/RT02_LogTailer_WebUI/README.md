# Log Tailer Web UI (RT02)

Tail log files in real-time and expose them over a small Web UI using `aiohttp` and WebSockets.

## Features
- Tail a file and stream new lines to connected browsers
- Demo mode produces a small static HTML page and sample lines

## Setup
```
pip install -r requirements.txt
```

## Run (demo)
```
python main.py --demo
```

Screenshot: `screenshots/screenshot.png`
# RT02 — Log Tailer + Web UI

Serves a tiny web UI and broadcasts appended lines from `application.log` over WebSocket.

Run demo:

```bash
python main.py --demo
```

Requirements:

```bash
pip install aiohttp
```

Screenshots: `screenshots/screenshot.png`
