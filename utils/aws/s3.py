import boto3
from botocore.exceptions import ClientError
import os
import uvicorn
import logging

logger = logging.getLogger("uvicorn")

aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_key = os.environ.get("AWS_SECRET_KEY")
aws_region = "ap-northeast-2"
s3_bucket_name = "chae-bucket"
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key, 
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)

async def s3_download(key: str):
    try:
        local_file_path = os.path.join("tmp/aws", key)  # 로컬 파일 경로 설정
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # 디렉토리 생성

        # S3 객체 다운로드
        s3.download_file(s3_bucket_name, key, local_file_path)
        return s3.get_object(Bucket=s3_bucket_name, Key=key)['Body'].read()
    except ClientError as err:
        print(str(err))

async def download(group_key: str | None = None):
    if not group_key:
        logger.info("FAIL")
        return "FAIL"
    response = s3.list_objects(Bucket=s3_bucket_name, Prefix=group_key)
    objects = response.get("Contents", [])
    logger.info(objects)
    object_keys = [obj["Key"] for obj in objects]
    logger.info(object_keys)
    contents = [await s3_download(key=obj_key) for obj_key in object_keys]
    logger.info("SUCCESS")
    return "SUCCESS"

async def s3_upload(local_file_path: str, s3_object_key: str):
    try:
        s3.upload_file(local_file_path, s3_bucket_name, s3_object_key)
    except ClientError as err:
        print(str(err))
        raise Exception(f"Failed to upload to S3: {str(err)}")

async def upload(file_name: str, saved_key: str | None = None) :
    #local_file_path = os.path.join("tmp", file_name)
    try:
        # S3에 업로드
        s3_object_key = "uploads/" + saved_key
        await s3_upload(file_name, s3_object_key)

        return s3_object_key
    except FileNotFoundError:
        raise Exception("File not found")

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)