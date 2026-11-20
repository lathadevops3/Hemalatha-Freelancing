import argparse
from pathlib import Path
import sys

try:
    import boto3
    from botocore.exceptions import NoCredentialsError, ClientError
except Exception:
    boto3 = None

REGION = "us-east-1"


def list_ec2():
    if boto3 is None:
        print("boto3 not installed or not available. Install requirements.txt to use AWS functions.")
        return
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        resp = ec2.describe_instances()
        print("EC2 Instances:")
        for r in resp.get("Reservations", []):
            for i in r.get("Instances", []):
                print(f"  {i['InstanceId']} - {i['State']['Name']} - {i.get('InstanceType')}")
    except NoCredentialsError:
        print("AWS credentials not configured. Skipping EC2 listing.")
    except ClientError as e:
        print(f"EC2 error: {e}")


def create_s3_bucket(bucket_name):
    if boto3 is None:
        print("boto3 not installed or not available.")
        return
    s3 = boto3.client("s3", region_name=REGION)
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": REGION})
        print(f"Created bucket: {bucket_name}")
    except ClientError as e:
        print(f"S3 error: {e}")


def upload_file(bucket_name, file_path):
    if boto3 is None:
        print("boto3 not installed or not available.")
        return
    s3 = boto3.client("s3", region_name=REGION)
    try:
        s3.upload_file(str(file_path), bucket_name, Path(file_path).name)
        print(f"Uploaded {file_path} -> s3://{bucket_name}/{Path(file_path).name}")
    except ClientError as e:
        print(f"Upload error: {e}")


def demo():
    print("AWS EC2 & S3 Automation Demo")
    print("Demo mode: AWS credentials and network calls are intentionally skipped.")
    print("[SIMULATION] EC2: i-0123456789abcdef0 - running - t3.micro")
    print("[SIMULATION] S3: bucket demo-bucket-for-portfolio-example - ready")

    sample = Path(__file__).parent / "sample_upload.txt"
    sample.write_text("Sample upload file for AWS S3 demo", encoding="utf-8")
    print(f"[SIMULATION] Uploaded {sample.name} -> s3://demo-bucket-for-portfolio-example/{sample.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        print("Run with --demo to execute a safe demo (no permanent changes).")


if __name__ == "__main__":
    main()
