import boto3
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def upload_to_s3(local_path, s3_key):
    try:
        s3_client.upload_file(local_path, settings.AWS_BUCKET_NAME, s3_key)
        return f"s3://{settings.AWS_BUCKET_NAME}/{s3_key}"
    except Exception as e:
        raise RuntimeError(f"S3 upload failed: {str(e)}")
