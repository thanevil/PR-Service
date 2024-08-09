import os
import requests
import boto3
from datetime import datetime


aws_region = os.environ.get('AWS_REGION')
repo_name = os.environ.get('REPO_NAME')
pr_number = os.environ.get('PR_NUMBER')
github_token = os.environ.get('GITHUB_TOKEN')


session = boto3.Session(region_name=aws_region)
s3_client = session.client('s3')


bucket_name = 'pr-service-bucket-cp'


api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"


headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}


response = requests.get(api_url, headers=headers)
response.raise_for_status()


changed_files = [file['filename'] for file in response.json()]


log_file_name = f"{repo_name}.log"


log_directory = os.path.dirname(log_file_name)
if log_directory and not os.path.exists(log_directory):
    os.makedirs(log_directory)


with open(log_file_name, 'w') as log_file:
    log_file.write("Changed files:\n")
    for file_path in changed_files:
        log_file.write(f"{file_path}\n")


current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


s3_key = f"{repo_name}/{current_time}/{log_file_name}"


s3_client.upload_file(log_file_name, bucket_name, s3_key)
print(f"Uploaded log file to {bucket_name}/{s3_key}")
print("All changed files have been processed and logged.")
