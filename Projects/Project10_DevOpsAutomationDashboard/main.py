import argparse
from pathlib import Path
import subprocess
import sys

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

REGION = "us-east-1"
LOG_FILE = Path(__file__).parent / "sample_logs.txt"
ALERT_FILE = Path(__file__).parent / "alert_summary.txt"


def list_ec2_instances():
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        response = ec2.describe_instances()
        print("EC2 Instances:")
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print(
                    f"  {instance['InstanceId']} - {instance['State']['Name']} - {instance['InstanceType']} - {instance['Placement']['AvailabilityZone']}"
                )
    except NoCredentialsError:
        print("AWS credentials are not configured. Skipping EC2 listing.")
    except ClientError as e:
        print(f"Error listing instances: {e}")


def start_ec2_instances(instance_ids):
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        ec2.start_instances(InstanceIds=instance_ids)
        print(f"Started: {', '.join(instance_ids)}")
    except NoCredentialsError:
        print("AWS credentials are not configured. Cannot start instances.")
    except ClientError as e:
        print(f"Error starting instances: {e}")


def stop_ec2_instances(instance_ids):
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Stopped: {', '.join(instance_ids)}")
    except NoCredentialsError:
        print("AWS credentials are not configured. Cannot stop instances.")
    except ClientError as e:
        print(f"Error stopping instances: {e}")


def create_s3_bucket(bucket_name):
    try:
        s3 = boto3.client("s3", region_name=REGION)
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
        print(f"Created S3 bucket: {bucket_name}")
    except NoCredentialsError:
        print("AWS credentials are not configured. Cannot create bucket.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


def upload_file_to_s3(bucket_name, file_path):
    try:
        s3 = boto3.client("s3", region_name=REGION)
        s3.upload_file(str(file_path), bucket_name, Path(file_path).name)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{Path(file_path).name}")
    except NoCredentialsError:
        print("AWS credentials are not configured. Cannot upload file.")
    except ClientError as e:
        print(f"Error uploading file: {e}")


def docker_status():
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Status}}"], capture_output=True, text=True)
        print("Docker containers:")
        print(result.stdout.strip())
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.")


def kubernetes_status():
    try:
        result = subprocess.run(["kubectl", "get", "pods", "--all-namespaces"], capture_output=True, text=True)
        print("Kubernetes pods:")
        print(result.stdout.strip())
    except FileNotFoundError:
        print("kubectl is not installed or not available in PATH.")


def system_health():
    print("System health:")
    if sys.platform == "win32":
        subprocess.run(["systeminfo"])
    else:
        subprocess.run(["uname", "-a"])
        subprocess.run(["uptime"])


def ensure_sample_logs():
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "2026-07-04 10:00:01 INFO Service started\n"
            "2026-07-04 10:01:20 ERROR Database connection failed\n"
            "2026-07-04 10:03:40 WARNING Disk space low\n"
            "2026-07-04 10:05:12 INFO User logged in\n"
            "2026-07-04 10:07:33 ERROR API timeout\n"
        )


def analyze_logs():
    ensure_sample_logs()
    lines = LOG_FILE.read_text().splitlines()
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = []
    for line in lines:
        for level in counts:
            if f" {level} " in line:
                counts[level] += 1
                if level == "ERROR":
                    errors.append(line)
    print("Log summary:")
    for level, count in counts.items():
        print(f"  {level}: {count}")
    most_frequent = max(set(errors), key=errors.count) if errors else None
    if most_frequent:
        print(f"Most frequent error: {most_frequent}")
    ALERT_FILE.write_text("\n".join(errors), encoding="utf-8")
    print(f"Saved error log summary to {ALERT_FILE}")


def send_alert_email(subject, body, recipients):
    print("Email alert placeholder")
    print(f"Subject: {subject}")
    print(f"Recipients: {', '.join(recipients)}")
    print(f"Body:\n{body}")


def main():
    parser = argparse.ArgumentParser(description="DevOps Automation Dashboard")
    parser.add_argument("--demo", action="store_true", help="Run a demo of dashboard capabilities")
    args = parser.parse_args()

    if args.demo:
        print("DevOps Automation Dashboard Demo")
        list_ec2_instances()
        docker_status()
        kubernetes_status()
        system_health()
        analyze_logs()
        send_alert_email(
            "DevOps Dashboard Alert",
            "This is a sample alert generated by the DevOps dashboard.",
            ["admin@example.com"],
        )
        print("Demo complete.")
    else:
        print("Run with --demo to see available dashboard capabilities.")


if __name__ == "__main__":
    main()
