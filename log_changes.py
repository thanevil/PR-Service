import os
import boto3
from datetime import datetime


aws_region = os.environ.get('AWS_REGION')
changed_files = os.environ.get('CHANGED_FILES').split()
repo_name = os.environ.get('REPO_NAME')


session = boto3.Session(region_name=aws_region)
s3_client = session.client('s3')


bucket_name = 'pr-service-bucket-alex'


log_file_name = f"{repo_name}.log"


log_directory = os.path.dirname(log_file_name)
if log_directory and not os.path.exists(log_directory):
    os.makedirs(log_directory)

with open(log_file_name, 'w') as log_file:
    log_file.write("Changed files:\n")
    for file_path in changed_files:
        if os.path.isfile(file_path):
            log_file.write(f"{file_path}\n")
        else:
            log_file.write(f"Skipped {file_path} as it does not exist.\n")

current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
s3_key = f"{repo_name}/{current_time}/{log_file_name}"
s3_client.upload_file(log_file_name, bucket_name, s3_key)
print(f"Uploaded log file to {bucket_name}/{s3_key}")
print("All changed files have been processed and logged.")
