# Kubernetes Health Checker

## Description
Wraps kubectl health checks to report pod and cluster health clearly.

## Real-World Scenario
Use this project to monitor Kubernetes clusters and detect unhealthy pods quickly.

## Features
- Fetch pod status
- Summarize cluster health
- Demo mode when kubectl is unavailable

## Technologies Used
- Python 3
- subprocess
- kubectl

## How to Run
```bash
python main.py --demo
```

## Sample Input
A Kubernetes context and namespace to inspect.

## Sample Output
A health summary report and pod status output.

## Screenshots
- `demo.gif`
- `screenshot.png`
