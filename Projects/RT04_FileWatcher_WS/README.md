# File Watcher → WebSocket Notifier

## Description
Watches a folder for changes and sends real-time notifications to browser clients.

## Real-World Scenario
Use this project for live file-monitoring dashboards or event-driven automation workflows.

## Features
- Monitor file creation events
- Broadcast notifications over WebSocket
- Fallback demo mode when watchdog is unavailable

## Technologies Used
- Python 3
- watchdog
- websockets
- asyncio

## How to Run
```bash
python main.py --demo
```

## Sample Input
A watched folder where new files are created or updated.

## Sample Output
Real-time create event notifications streamed to connected clients.

## Screenshots
- `demo.gif`
- `screenshot.png`
