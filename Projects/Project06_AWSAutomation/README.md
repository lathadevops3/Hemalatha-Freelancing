# Project 6 – AWS Automation

A menu-driven AWS automation tool for common cloud operations.

## Features

- List EC2 instances
- Start EC2 instances
- Stop EC2 instances
- Create S3 buckets
- Upload files to S3

## Requirements

- `boto3`
- AWS credentials configured in `~/.aws/credentials` or environment variables

## Usage

1. Install dependencies:

```bash
pip install boto3
```

2. Run the tool:

```bash
python main.py
```

3. Follow the menu prompts.

## Notes

- This tool uses the default AWS profile.
- Ensure your IAM user has EC2 and S3 permissions.
- Update `REGION` in `main.py` if you need a different AWS region.
