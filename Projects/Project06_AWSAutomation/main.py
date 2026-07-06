import argparse
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"


def start_ec2_instances(instance_ids):
    ec2 = boto3.client("ec2", region_name=REGION)
    try:
        response = ec2.start_instances(InstanceIds=instance_ids)
        print("Starting instances:")
        for instance in response.get("StartingInstances", []):
            print(f"  {instance['InstanceId']} -> {instance['CurrentState']['Name']}")
    except ClientError as e:
        print(f"Error starting instances: {e}")


def stop_ec2_instances(instance_ids):
    ec2 = boto3.client("ec2", region_name=REGION)
    try:
        response = ec2.stop_instances(InstanceIds=instance_ids)
        print("Stopping instances:")
        for instance in response.get("StoppingInstances", []):
            print(f"  {instance['InstanceId']} -> {instance['CurrentState']['Name']}")
    except ClientError as e:
        print(f"Error stopping instances: {e}")


def list_ec2_instances():
    ec2 = boto3.client("ec2", region_name=REGION)
    try:
        response = ec2.describe_instances()
        print("EC2 Instances:")
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print(
                    f"  ID: {instance['InstanceId']}, State: {instance['State']['Name']}, Type: {instance['InstanceType']}, AZ: {instance['Placement']['AvailabilityZone']}"
                )
    except ClientError as e:
        print(f"Error listing instances: {e}")


def create_s3_bucket(bucket_name):
    s3 = boto3.client("s3", region_name=REGION)
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
        print(f"Created S3 bucket: {bucket_name}")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


def upload_file_to_s3(bucket_name, file_path, object_name=None):
    s3 = boto3.client("s3", region_name=REGION)
    object_name = object_name or file_path.name
    try:
        s3.upload_file(str(file_path), bucket_name, object_name)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{object_name}")
    except ClientError as e:
        print(f"Error uploading file: {e}")


def print_menu():
    print("AWS Automation Tool")
    print("1. List EC2 instances")
    print("2. Start EC2 instances")
    print("3. Stop EC2 instances")
    print("4. Create S3 bucket")
    print("5. Upload file to S3")
    print("0. Exit")


def main(auto_exit: bool = False, auto_choice: str | None = None):
    while True:
        print_menu()
        if auto_choice is not None:
            choice = auto_choice
            print(f"Choose an option: {choice}")
        else:
            choice = input("Choose an option: ").strip()

        if choice == "1":
            list_ec2_instances()
        elif choice == "2":
            if auto_choice is not None:
                instance_ids = []
            else:
                instance_ids = input("Enter instance IDs (comma-separated): ").split(",")
                instance_ids = [id_.strip() for id_ in instance_ids if id_.strip()]
            start_ec2_instances(instance_ids)
        elif choice == "3":
            if auto_choice is not None:
                instance_ids = []
            else:
                instance_ids = input("Enter instance IDs (comma-separated): ").split(",")
                instance_ids = [id_.strip() for id_ in instance_ids if id_.strip()]
            stop_ec2_instances(instance_ids)
        elif choice == "4":
            if auto_choice is not None:
                bucket_name = "test-bucket-example"
            else:
                bucket_name = input("Enter new S3 bucket name: ").strip()
            create_s3_bucket(bucket_name)
        elif choice == "5":
            if auto_choice is not None:
                bucket_name = "test-bucket-example"
                file_path = Path(__file__).parent / "test_upload.txt"
                file_path.write_text("Test upload file.", encoding="utf-8")
            else:
                bucket_name = input("Enter S3 bucket name: ").strip()
                file_path = Path(input("Enter local file path: ").strip())
            upload_file_to_s3(bucket_name, file_path)
        elif choice == "0":
            break
        else:
            print("Invalid option. Try again.")

        if auto_exit:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Automation Tool")
    parser.add_argument("--auto-exit", action="store_true", help="Run once and exit automatically after the first menu iteration")
    parser.add_argument("--auto-choice", choices=["0", "1", "2", "3", "4", "5"], help="Automatically choose a menu option")
    args = parser.parse_args()
    main(auto_exit=args.auto_exit, auto_choice=args.auto_choice)
