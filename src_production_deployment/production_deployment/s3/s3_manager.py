from __future__ import annotations
from pathlib import Path
from src_production_deployment.production_deployment.aws_session_prod import AWSSession
from botocore.exceptions import ClientError
from src_production_deployment.configs.config import AWSBUCKET
import io
import pandas as pd

class S3Manager():
    def __init__(self,session: AWSSession):
        self._session = session
        self._client = session.boto_session.client("s3")
        self.bucket = AWSBUCKET


    @property
    def default_sm_bucket(self):
        return self._session.default_bucket

    def upload_file(self,local_path:str, bucket:str,s3_key:str):
        self._client.upload_file(filename = str(Path(local_path)) , Bucket = bucket , Key=s3_key)

    def object_exists(self, bucket: str, s3_key: str):

        try:
            self._client.head_object(Bucket=bucket, Key=s3_key)
            return True

        except ClientError:
            return False

    
    def delete_file(self, bucket: str, s3_key: str):
        self._client.delete_object(Bucket=bucket, Key=s3_key)
        print(f"Deleted Successfully - {s3_key}")

    def upload_file_memory(self,data,key):
        self._client.upload_fileobj(data, Bucket = self.bucket , Key = key)


    def upload_champion_model_s3(self, local_directory:str, s3_prefix:str):
        local_directory = Path(local_directory)
        for file_path in local_directory.rglob("*"):
            if file_path.is_file(): # "Only process this item if it is an actual file."
                relative_path = file_path.relative_to(local_directory) # it removes comman parent
                s3_key = f"{s3_prefix}/{relative_path.as_posix()}" # converts: data\model.pkl into data/model.pkl
                self._client.upload_file(Filename=str(file_path), Bucket=self.bucket, Key=s3_key)

    def read_file(self, s3_key:str) -> pd.DataFrame:
            response = self._client.get_object( Bucket = self.bucket ,Key=s3_key)
            data = response["Body"].read()
            return pd.read_parquet(io.BytesIO(data))


