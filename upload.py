import boto3
import os
from decouple import config

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

S3_BUCKET_NAME = config('S3_BUCKET_NAME')


s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

bucket_name = S3_BUCKET_NAME # Dev
subfolder = "images"


def upload_to_s3(file_path, filename):
    object_name = filename
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print("Upload Successful")
        return True
    except ClientError as e:
        print("Upload Failed")
        print(e)
        return False

def get_s3_object_url(object_name):
    return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

def upload_all_files_from_subfolder(subfolder):
    urls = []
    for filename in os.listdir(subfolder):
        file_path = os.path.join(subfolder, filename)
        if os.path.isfile(file_path) and upload_to_s3(file_path, filename):
            url = get_s3_object_url(filename)
            urls.append(url)
    return urls

urls = upload_all_files_from_subfolder(subfolder)
with open("object_urls.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")
