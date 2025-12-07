import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()  # loads from .env


print("Loaded ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("Loaded Secret:", "YES" if os.getenv("AWS_SECRET_ACCESS_KEY") else "NO")
print("Loaded Region:", os.getenv("AWS_REGION"))
print("Loaded Bucket:", os.getenv("AWS_BUCKET_NAME"))


def test_s3():
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        bucket = os.getenv("AWS_BUCKET_NAME")
        resp = s3.list_objects_v2(Bucket=bucket)
        print("Success:", resp.get("KeyCount", 0))
    except ClientError as e:
        print("AWS error:", e)
    except Exception as e:
        print("Failure:", e)

if __name__ == "__main__":
    test_s3()
