# AWS Automation

## Description
Automates AWS EC2 and S3 operations using boto3 with demo fallback for safe portfolio display.

## Real-World Scenario
Use this tool to manage cloud instances and storage with simple automation commands.

## Features
- List EC2 instances and S3 buckets
- Create buckets and upload files
- Demo mode for environments without AWS credentials

## Technologies Used
- Python 3
- boto3

## How to Run
```bash
python main.py --demo
```

## Sample Input
AWS credentials and a target bucket name for file upload.

## Sample Output
A log of EC2/S3 operations or a demo output file when credentials are unavailable.

## Screenshots
- `screenshot.png`
