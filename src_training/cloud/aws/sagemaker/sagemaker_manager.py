from sagemaker.tuner import HyperparameterTuner
from src_training.tuning.parameter_space.parameter_space_converter import ParameterSpaceConverter
from src_training.cloud.aws.sagemaker.estimator_factory import SageMakerEstimatorFactory
from src_training.cloud.aws.aws_session import AWSSession
from src_training.cloud.aws.sagemaker.estimator_config import SageMakerEstimatorConfig


class SageMakerManager:
    '''uses that estimator to start tuning jobs'''
    
    def __init__(self, aws_session: AWSSession, execution_role:str):
        self._aws_session = aws_session 
        self._role = execution_role
        self._session = aws_session.sagemaker_session
        self._client = aws_session.boto_session.client("sagemaker")

    def start_hyperparamter_tuning_job(
                        self,
                        algorithm,
                        parameter_space: dict,
                        input_channels: dict,
                        estimator_config: SageMakerEstimatorConfig,
                        objective_metric_name: str,
                        objective_type: str,
                        max_jobs: int,
                        max_parallel_jobs: int,
                        job_name: str,
                    ):
        """
        Starts a SageMaker Hyperparameter Tuning Job.
        """
        hyperparameter_ranges = ParameterSpaceConverter.to_sagemaker(parameter_space)

        estimator = SageMakerEstimatorFactory.create(algorithm = algorithm , estimator_config=estimator_config)
        print(estimator.metric_definitions)
    
        tuner = HyperparameterTuner(estimator = estimator, 
                                    objective_metric_name = objective_metric_name,
                                    hyperparameter_ranges = hyperparameter_ranges,
                                    objective_type=objective_type,
                                    max_jobs = max_jobs, 
                                    metric_definitions=estimator_config.metric_definitions,
                                    max_parallel_jobs = max_parallel_jobs,
                                    early_stopping_type="Auto")
 
        # Start the SageMaker Hyperparameter Tuning Job.
            #
            # SageMaker now:
            # 1. Launches one or more training jobs.
            # 2. Creates the required EC2 training instances.
            # 3. Downloads the datasets from S3.
            # 4. Executes train.py on each training instance.
            # 5. Collects the validation metric.
            # 6. Chooses the next hyperparameters.
            # 7. Repeats until max_jobs is reached.

        tuner.fit(inputs = input_channels, job_name = job_name, wait = True)

        return tuner


    def start_hyperparamter_tuning_job_no_hyper(
                            self,
                            algorithm,
                            input_channels: dict,
                            estimator_config: SageMakerEstimatorConfig,
                            objective_metric_name: str,
                            objective_type: str,
                            max_jobs: int,
                            max_parallel_jobs: int,
                            job_name: str,
                        ):
        """
        Starts a SageMaker Hyperparameter Tuning Job.
        """

        estimator = SageMakerEstimatorFactory.create(algorithm = algorithm , estimator_config = estimator_config)

        print(estimator.metric_definitions)

        '''
        estimator.fit(objective_metric_name = objective_metric_name,
                      objective_type=objective_type,
                      max_jobs = max_jobs, 
                      metric_definitions=estimator_config.metric_definitions,
                      max_parallel_jobs = max_parallel_jobs)
        '''
    


        estimator.fit(inputs = input_channels, job_name = job_name, wait = True)

        return estimator


'''
So inside SageMakerManager you now have two different objects

1. self._session

    This is: sagemaker.Session(...)

    High-level SageMaker SDK object.

        Used for:
        SKLearn
        Uploading data
        Default bucket
        Managing training jobs through the SDK


2. self._client - This is boto3.client("sagemaker")

    Low-level AWS API client.

    Used for operations like:

    describe_training_job()
    list_training_jobs()
    describe_hyper_parameter_tuning_job()
    Any SageMaker API that the SDK doesn't wrap conveniently.
'''