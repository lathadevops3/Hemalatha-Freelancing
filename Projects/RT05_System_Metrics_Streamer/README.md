# System Metrics Streamer

## Description
Streams live CPU and memory metrics over WebSocket for real-time infrastructure monitoring.

## Real-World Scenario
Use this tool for telemetry dashboards that display system health during load testing.

## Features
- Capture CPU and memory usage
- Stream metrics live over WebSocket
- Demo mode prints sample metric snapshots

## Technologies Used
- Python 3
- psutil
- websockets
- asyncio

## How to Run
```bash
python main.py --demo
```

## Sample Input
A local machine to monitor or demo mode for sample data.

## Sample Output
A stream of system metric snapshots printed or broadcast in real time.

## Screenshots
- `demo.gif`
- `screenshot.png`
