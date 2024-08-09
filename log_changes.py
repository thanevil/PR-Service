import os
import requests
import boto3
from datetime import datetime

# Set up environment variables for AWS and GitHub
aws_region = os.environ.get('AWS_REGION')
repo_name = os.environ.get('REPO_NAME')
pr_number = os.environ.get('PR_NUMBER')
github_token = os.environ.get('GITHUB_TOKEN')

# Initialize AWS S3 client
session = boto3.Session(region_name=aws_region)
s3_client = session.client('s3')

# Define your S3 bucket name
bucket_name = 'pr-service-bucket-cp'

# GitHub API URL to get changed files in the pull request
api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"

# Headers for the GitHub API request
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Make the request to get the list of changed files
response = requests.get(api_url, headers=headers)
response.raise_for_status()  # Raise an exception for HTTP errors

# Extract the changed files from the response
changed_files = [file['filename'] for file in response.json()]

# Create a log file with the repository name
log_file_name = f"{repo_name}_log.txt"

# Ensure the directory for the log file exists
log_directory = os.path.dirname(log_file_name)
if log_directory and not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Write the list of changed files to the log file
with open(log_file_name, 'w') as log_file:
    log_file.write("Changed files:\n")
    for file_path in changed_files:
        log_file.write(f"{file_path}\n")

# Get current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Define S3 key with repository name, date, and time
s3_key = f"{repo_name}/{current_time}/{log_file_name}"

# Upload the log file to S3
s3_client.upload_file(log_file_name, bucket_name, s3_key)
print(f"Uploaded log file to {bucket_name}/{s3_key}")
print("All changed files have been processed and logged.")
