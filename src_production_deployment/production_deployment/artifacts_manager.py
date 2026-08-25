from pathlib import Path
from src_production_deployment.production_deployment.s3.s3_manager import S3Manager
from sagemaker.inputs import TrainingInput

class ArtifactManager:
    def __init__(self,s3_manager:S3Manager, bucket:str):
        self._s3 = s3_manager
        self._bucket = bucket

    def upload_dataset(self,dataset_name:str , dataset_path:str, stage:str = "raw")-> str:
        path = Path(dataset_path)
        s3_key = f"datasets/{dataset_name}/{stage}/{path.name}"
        self._s3.upload_file(local_path=str(path), bucket=self._bucket, s3_key=s3_key,)
        return s3_key

    def upload_model(self, model_path: str, algorithm: str, version: str) -> str:
        path = Path(model_path)
        s3_key = f"models/{algorithm}/{version}/{path.name}"
        self._s3.upload_file(local_path=str(path), bucket=self._bucket, s3_key=s3_key)
        return s3_key

    def download_model(self, algorithm: str, version: str, file_name: str, local_path: str):
        s3_key = f"models/{algorithm}/{version}/{file_name}"
        self._s3.download_file(
            bucket=self._bucket,
            s3_key=s3_key,
            local_path=local_path,
        )

    def upload_processed_dataset(self, dataset_name:str, dataset_directory:str) -> dict[str,str]:

        dataset_directory = Path(dataset_directory)

        print(dataset_directory)

        for file in dataset_directory.glob("*.parquet"):

            self.upload_dataset(dataset_name = dataset_name, dataset_path=str(file), stage="processed",)
            
        return f"s3://{self._bucket}/datasets/{dataset_name}/processed/"
     

    def get_dataset_uri(self, dataset_name: str, stage: str, file_name: str,) -> str:

        s3_key = f"datasets/{dataset_name}/{stage}/{file_name}"

        return f"s3://{self._bucket}/{s3_key}"

    def get_processed_dataset_uri(self,dataset_name:str) -> str:
        return f"s3://{self._bucket}/datasets/{dataset_name}/processed/"

    def get_training_input(self,dataset_name:str) -> TrainingInput:
        return TrainingInput(s3_data=self.get_processed_dataset_uri(dataset_name),
                             content_type="application/x-parquet",)

    def upload_champion_model_s3(self, local_directory:str, s3_prefix:str):
        local_directory = Path(local_directory)
        for file_path in local_directory.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_directory)
                s3_key = f"{s3_prefix}/{relative_path.as_posix()}"
                self._client.upload_file(Filename=str(file_path), Bucket=self.bucket, Key=s3_key)
                

        


