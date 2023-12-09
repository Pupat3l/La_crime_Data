# %% import necessary library
import boto3
import psycopg2
from botocore.exceptions import ClientError

# %%
bucket_name = "bucket-name"
folder_path = "cleaned/"
access_key = 'key'
secret_key = 'key'

# %%
# Create an S3 client
s3=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)

# List objects in the specified folder
response = s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix=folder_path
)

# Extract file names from the response
file_names = [obj['Key'] for obj in response.get('Contents', [])]
file_names

# %%
# Redshift Serverless connection details
endpoint = 'endpoint'
port = '5439'  # default Redshift port
database = 'db'
user = 'admin-user'
password = 'password'
timeout=60

# %%
conn_string = f"dbname='{database}' user='{user}' host='{endpoint}' password='{password}' port='{port}' connect_timeout={timeout}"

# %%
conn = psycopg2.connect(conn_string)

# %%
def load_data(copy_cmd):
    # Assuming you already have a connection and cursor (conn and cur) established
    # inserted try block to avoid errors
    cur = conn.cursor()
    try:
        cur.execute(copy_cmd)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()

# %%
schema="schema"
region="region"
iam_role='role_arn'

# %%
for i in file_names:
    slash=i.index('/')+1
    dot=i.index('.')
    table=i[slash:dot]
    print(table)
    copy_cmd = f"""
    COPY {database}.{schema}.{table}
    FROM 's3://{bucket_name}/{i}'
    IAM_ROLE '{iam_role}'
    FORMAT AS CSV DELIMITER ',' QUOTE '"' IGNOREHEADER 1 REGION AS '{region}';
    """
    print('Start Loading')
    print(copy_cmd)
    load_data(copy_cmd)
    print('SUCCESS')

    

# %%
conn.close()


