from src_training.cloud.aws.s3.s3_manager import S3Manager
from src_production_deployment.production_deployment.artifacts_manager import ArtifactManager
from src_training.cloud.aws.sagemaker.sagemaker_manager import SageMakerManager
from src_training.cloud.aws.aws_session import AWSSession
from src_training.cloud.aws.config.sagemaker_tuning_config import SageMakerTuningConfig
from src_training.cloud.aws.sagemaker.estimator_config import SageMakerEstimatorConfig
from configs.project_config import AWSBUCKET , EXECUTION_ROLE
from src_training.ensemble.tuning_enum import TuningStrategy
from datetime import datetime

class TuningConfigFactory:

    @staticmethod
    def create(strategy):

        if strategy == TuningStrategy.SAGEMAKER:
            ''' building the dependencies needed to execute a SageMaker tuning job.'''
            '''
            your pipeline should eventually do something like:
            Train model on AWS SageMaker
                │
                ▼
            Upload data to S3
                │
                ▼
            Start SageMaker Hyperparameter Tuning Job
                │
                ▼
            Wait for completion
                │
                ▼
            Download best parameters
            To accomplish this, your code needs below services.

            '''


            # 1.Create AWS Session. Think of this as logging into AWS. Without it, you cannot access: S3 , Sagemaker or any service
            session = AWSSession() # 

            # 2. Create S3 Manager  - Because SageMaker cannot access your local laptop files.
            # All file writes operation in s3 bucket is taken care by S3 maager
            s3_manager = S3Manager(session)

            # 3. Think of this as organizing your project files. It manages where artifacts are stored.
            artifact_manager = ArtifactManager(s3_manager = s3_manager, bucket = AWSBUCKET)

            # 4. This is the component that actually talks to SageMaker.
            # It does things like: create_estimator() , create_tuner() , fit()
            sagemaker_manager = SageMakerManager(aws_session = session , execution_role = EXECUTION_ROLE)

            # 5. SageMakerEstimatorConfig describes how SageMaker should train your model.
            sagemaker_estimator_config = SageMakerEstimatorConfig(
                                                                    entry_point="ensemble/pipelines/stacking_pipeline.py", 
                                                                    # This tells SageMaker: "When the training instance starts, execute this Python file."
                                                                    source_dir="src/cloud/aws/sagemaker",
                                                                    role=EXECUTION_ROLE,
                                                                    framework_version="1.4-2",
                                                                    py_version="py3",
                                                                    instance_type="ml.m5.xlarge",
                                                                    instance_count=1,
                                                                    sagemaker_session= session.sagemaker_session,
                                                                    # This is your connection to SageMaker.
                                                                    metric_definitions = [
                                                                                            {
                                                                                                "Name": "validation:rmse",
                                                                                                "Regex": r"validation:rmse=([0-9\.]+)"
                                                                                            }
                                                                                        ],
                    
                                                                    hyperparameters={}
                                                                    )
                                                                    

            return SageMakerTuningConfig(
                                        dataset_name = "DemandForecasting",
                                        artifact_manager = artifact_manager,
                                        sagemaker_manager = sagemaker_manager,
                                        estimator_config = sagemaker_estimator_config,
                                        objective_metric_name = "validation:rmse",
                                        objective_type = "Minimize",
                                        max_jobs = 20,
                                        max_parallel_jobs = 2,
                                        job_name=f"Ensemble-stacking-{datetime.now():%Y%m%d-%H%M%S}"
                                        )

        return None