# %%
#pip install boto3

# %%
import boto3


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
s3_key = "landing/data.csv"
access_key = 'xyz'
secret_key = 'xyz'

# Upload the file to S3
upload_to_s3(local_file_path, s3_bucket_name, s3_key, access_key,secret_key)
