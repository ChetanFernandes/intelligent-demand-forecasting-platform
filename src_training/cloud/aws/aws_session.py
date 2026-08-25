from __future__  import annotations
import boto3
import sagemaker

class AWSSession:
     """
    Central AWS session manager.

    This class owns the boto3 session and the SageMaker session.

    Every AWS service in our platform will use this object.
    """
     def __init__(self, region_name:str = "us-east-1") -> None:
        self._boto_session = boto3.Session(region_name=region_name) 
        # Created a session with AWS. Before you create any AWS service, you need a Session.
        self._sm_session = sagemaker.Session(boto_session = self._boto_session)

     @property
     def boto_session(self):
        return self._boto_session

     @property
     def sagemaker_session(self):
        return self._sm_session
 

     @property
     def region(self):
        return self._boto_session.region_name

     @property
     def default_sm_bucket(self):
        return self._sm_session.default_bucket()

'''
Use:

boto3.Session when you need low-level AWS services (S3, IAM, STS, EC2, etc.).
sagemaker.Session when you're working with SageMaker features like SKLearn, HyperparameterTuner, uploading training data, default buckets, and managing training jobs.

The SageMaker SDK is designed to make common ML workflows much simpler than using the raw Boto3 SageMaker client directly
'''