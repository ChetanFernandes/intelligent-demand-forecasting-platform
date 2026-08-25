from __future__ import annotations
import boto3
import sagemaker

class AWSSession:
    def __init__(self,region_name:str = "us-east-1")-> None:
        self._boto_session = boto3.Session(region_name=region_name)
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

    
