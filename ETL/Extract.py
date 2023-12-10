# %%
#pip install boto3

# %%
import boto3
import requests 

# %%
from botocore.exceptions import NoCredentialsError

# %%
def upload_to_s3(local_file, bucket_name, s3_file, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        print(f"Upload successful: {local_file} to {bucket_name}/{s3_file}")
        return True
    except FileNotFoundError:
        print(f"The file {local_file} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False


# %%
# Replace these variables with your own values
local_file_path = "local/path/to/data/file"
s3_bucket_name = "s3-bucket"
s3_key = "path/to/file"
access_key = 'xyz'
secret_key = 'xyz'

# Upload the file to S3
upload_to_s3(local_file_path, s3_bucket_name, s3_key, access_key,secret_key)


#function to upload from url for automation
def upload_from_url_to_s3(url, bucket_name, s3_key, aws_access_key_id, aws_secret_access_key):
    try:
        # Download the file from the URL
        response = requests.get(url)
        # Upload the file to S3
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3.put_object(Body=response.content, Bucket=bucket_name, Key=s3_key)
        
        print(f"Upload successful: {url} to {bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
url='https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'
upload_from_url_to_s3(url, s3_bucket_name, s3_key, access_key, secret_key)