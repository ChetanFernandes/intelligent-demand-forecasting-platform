from abc import ABC
from sagemaker.sklearn.estimator import SKLearn
from src_training.cloud.aws.sagemaker.estimator_config import SageMakerEstimatorConfig
from src_training.ensemble.tuning_enum import Algorithm


class SageMakerEstimatorFactory(ABC):
    '''creates the correct estimator object'''

    @staticmethod
    def create(algorithm: Algorithm, estimator_config: SageMakerEstimatorConfig):

        if algorithm in (Algorithm.LIGHTGBM , Algorithm.XGBOOST, Algorithm.CATBOOST, Algorithm.ENSEMBLE):

            config = estimator_config

            return SKLearn (

                entry_point = config.entry_point, # The Python script that SageMaker will execute.

                source_dir = config.source_dir, # The folder containing train.py and any supporting Python files. "src/cloud/sagemaker" # SageMaker uploads this entire folder to the training instance.

                role = config.role, # The IAM Role that gives SageMaker permission to access AWS resource

                framework_version = config.framework_version, # The version of the SageMaker Scikit-Learn container.

                py_version = config.py_version, # The Python version inside the training container
 
                instance_type =  config.instance_type, # The AWS machine that will perform the training.

                instance_count = config.instance_count,

                sagemaker_session = config.sagemaker_session, # A SageMaker session object that manages communication with AWS.

                metric_definitions = config.metric_definitions,

                hyperparameters = config.hyperparameters, # A dictionary of parameters passed to train.py.

                
            )
        print(config.metric_definitions)

        raise ValueError(f"Unsupported algorithm: {algorithm}")


    '''
    Your Laptop
      │
      ▼
Create SKLearn Estimator
      │
      ▼
Upload train.py
      │
      ▼
Upload source_dir
      │
      ▼
Launch EC2 instance
      │
      ▼
Install Scikit-Learn Environment
      │
      ▼
Download dataset from S3
      │
      ▼
Run train.py
      │
      ▼
Return metrics/logs
'''