import boto3
import sagemaker

# create a boto3 session
boto_session = boto3.Session(region_name = "ap-south-1")

# Create SageMaker session
sm_session = sagemaker.Session(boto_session=boto_session)

print("Connected to sagemaker")

print(f"Default Bucket : {sm_session.default_bucket()}")

print(f"Region : {boto_session.region_name}")
