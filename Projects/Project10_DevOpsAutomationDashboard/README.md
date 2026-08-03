# DevOps Automation Dashboard

## Description
Provides an overview of DevOps health by checking environment status and generating logs.

## Real-World Scenario
Use this dashboard to combine cloud, container, and log status checks into a single health summary.

## Features
- Check AWS, Docker, and Kubernetes status
- Analyze logs for alerts
- Produce dashboard summary files

## Technologies Used
- Python 3
- boto3
- subprocess
- logging

## How to Run
```bash
python main.py --demo
```

## Sample Input
A local environment with AWS/Docker/Kubernetes or demo fallback simulated status.

## Sample Output
A dashboard status report and alert summary text file.

## Screenshots
- `dashboard_status.png`
