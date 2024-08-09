import os
import boto3

# Set up environment variables for AWS and changed files
aws_region = os.environ.get('AWS_REGION')
changed_files = os.environ.get('CHANGED_FILES').split()
repo_name = os.environ.get('REPO_NAME')

# Initialize AWS S3 client with assumed role
session = boto3.Session(region_name=aws_region)
s3_client = session.client('s3')

# Define your S3 bucket name
bucket_name = 'your-s3-bucket-name'

# Upload changed files to S3
for file_path in changed_files:
    if os.path.isfile(file_path):
        s3_key = f"{repo_name}/{file_path}"
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to {bucket_name}/{s3_key}")
    else:
        print(f"Skipped {file_path} as it does not exist.")

print("All changed files have been processed.")
