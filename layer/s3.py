import boto3

# Initialize S3 resource once
s3_resource = boto3.resource('s3')


def read_file(bucket_name, file_key):
    obj = s3_resource.Object(bucket_name, file_key)
    file_content = obj.get()['Body'].read().decode('utf-8')
    return file_content

def write_file(bucket_name, file_key, data):
    obj = s3_resource.Object(bucket_name, file_key)
    obj.put(Body=data)
    print(f"File {file_key} written to bucket {bucket_name}.")


def download_file(bucket_name, file_key, local_file_path):
    # Define bucket name, file key, and local file path
    # bucket_name = "your-bucket-name"
    # file_key = "your/key/to/file.txt"
    # local_file_path = "local_file.txt"

    # Download the file
    s3_resource.Bucket(bucket_name).download_file(Key=file_key, Filename=local_file_path)


def iterate_files(bucket_name, prefix):
    # # Define bucket name and key prefix
    # bucket_name = "your-bucket-name"
    # prefix = "your/key/prefix/"  # Include trailing slash if needed

    # Get the bucket object
    bucket = s3_resource.Bucket(bucket_name)

    # List all files under the prefix
    for obj in bucket.objects.filter(Prefix=prefix):
        yield obj.key  # File path within the bucket