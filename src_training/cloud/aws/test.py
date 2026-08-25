from src_training.cloud.aws.aws_session import AWSSession
from src_training.cloud.aws.s3.s3_manager import S3Manager
from src_production_deployment.production_deployment.artifacts_manager import ArtifactManager

session = AWSSession()

s3 = S3Manager(session)

bucket = "faang-ml-platform"

artifact = ArtifactManager(s3_manager=s3, bucket=bucket)


print("Default_bucket")
print(session.default_sm_bucket)

print("Default region")
print(session.region)

print(" = " * 10)


response = s3.list_s3_buckets()
for bucket in response["Buckets"]:
    print(bucket["Name"])


'''
local_path = r"artifacts\datasets\train_df.parquet"

bucket = "faang-ml-platform-135053048192"

s3.delete_file(bucket = bucket, s3_key = "test/abc.txt")

s3.upload_file(local_path = local_path, bucket = bucket, s3_key = "test/abc.csv")

objects = s3.list_objects(bucket=bucket, prefix= "test/")
for obj in objects:
    print(obj["Key"])

result = s3.object_exists(bucket = bucket, s3_key = "test/abc.csv")
print(result)

dataset_directory = "artifacts/datasets/data_split"

dataset_name = "m5"

upload_files = artifact.upload_processed_dataset(dataset_name = dataset_name , dataset_directory = dataset_directory)

print(upload_files)
'''









