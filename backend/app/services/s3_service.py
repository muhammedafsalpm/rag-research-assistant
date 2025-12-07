import boto3
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def upload_to_s3(data, key, is_bytes=False):
    bucket = settings.AWS_BUCKET_NAME  # <-- use your env variable

    if is_bytes:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType="application/pdf"
        )
        return f"s3://{bucket}/{key}"

    # fallback: uploading from file path (not used now)
    with open(data, "rb") as f:
        s3_client.upload_fileobj(f, bucket, key)
