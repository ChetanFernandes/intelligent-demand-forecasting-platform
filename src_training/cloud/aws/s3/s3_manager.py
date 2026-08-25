from __future__ import annotations
from pathlib import Path
from src_training.cloud.aws.aws_session import AWSSession
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, session : AWSSession):
        self._session = session
        self._client = session.boto_session.client("s3") 
        # Since session is still available inside __init__(), there's no need to go through self._session.

    @property
    def default_sm_bucket(self):
        return self._session.default_bucket

    @property
    def default_region(self):
        return self._session.region

    def list_s3_buckets(self):
        return self._client.list_buckets()

    def upload_file(self, local_path: str, bucket: str, s3_key: str):
        self._client.upload_file(Filename=str(Path(local_path)), Bucket=bucket, Key=s3_key)
       

    def download_file(self, bucket: str, s3_key: str, local_path: str) -> None:
        """
        Download a file from S3.
        """
        local_path = Path(local_path)

        # Create parent directories if they don't exist

        local_path.parent.mkdir(parents=True, exist_ok=True)

        self._client.download_file(Bucket=bucket, Key=s3_key, Filename = str(local_path))

        print(f"Downloaded {s3_key} -> {local_path}")


    def list_objects(self, bucket: str, prefix: str = ""):
        response = self._client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return response.get("Contents", [])

    def object_exists(self, bucket: str, s3_key: str):

        try:
            self._client.head_object(Bucket=bucket, Key=s3_key)
            return True

        except ClientError:
            return False

    def delete_file(self, bucket: str, s3_key: str):
        self._client.delete_object(Bucket=bucket, Key=s3_key)
        print(f"Deleted Successfully - {s3_key}")