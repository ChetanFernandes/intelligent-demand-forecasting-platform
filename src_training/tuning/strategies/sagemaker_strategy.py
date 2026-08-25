from src_training.tuning.strategies.base_stratergy import BaseTuningStrategy
from configs.project_config import PROCESSED_DATASET_DIR
from sagemaker.inputs import TrainingInput
from sagemaker.tuner import HyperparameterTuner

class SageMakerStratergy(BaseTuningStrategy):

    def __init__(self, estimator , parameter_space, algorithm, sagemaker_manager, artifact_manager, estimator_config, dataset_name: str , 
                  objective_metric_name:str,objective_type:str,
                  max_jobs: int, max_parallel_jobs: int,job_name: str):
        
        self._estimator = estimator 
        self._parameter_space = parameter_space
        self._algorithm = algorithm
        self._sagemaker_manager = sagemaker_manager
        self._artifact_manager = artifact_manager
        self._estimator_config = estimator_config
        self._objective_metric_name = objective_metric_name
        self._objective_type = objective_type
        self._max_jobs = max_jobs
        self._max_parallel_jobs = max_parallel_jobs
        self._job_name = job_name
        self._dataset_name = dataset_name
        self._tuner = None

    def fit(self, job_name, X_train = None, Y_train = None):

        # To excute fit we need 
           # 1 - # Upload the processed datasets from the local machine to S3.
                 # SageMaker training instances cannot access files on the local machine,
                 # so the datasets must first be stored in S3.
           # 2 - # Provide the S3 location of the uploaded datasets to SageMaker.
                 # 'input_channels' tells the training job where to find the training data.
                #
                # Example:
                # input_channels = {
                #     "train": "s3://my-bucket/datasets/DemandForecasting/processed/"
                # }
           # 3. # Step 3:
                # Create and start the SageMaker Hyperparameter Tuning Job.
                #
                # This includes:
                # - Creating the SageMaker Estimator
                # - Creating the HyperparameterTuner
                # - Passing the hyperparameter search space
                # - Passing the S3 input channels
                # - Launching the tuning job
            

        processed_dataset_uri = self._artifact_manager.upload_processed_dataset(dataset_name=self._dataset_name, dataset_directory=PROCESSED_DATASET_DIR)

        #input_channels = {"train": processed_dataset_uri}

        try:
            self._tuner = HyperparameterTuner.attach(tuning_job_name = job_name)
            return self
        except:
            pass


        input_channels = { "train": self._artifact_manager.get_training_input(self._dataset_name)}
            
        # Calling method start_hyperparamter_tuning_job from class _sagemaker_manager
        ''' 
        self._tuner = self._sagemaker_manager.start_hyperparamter_tuning_job(
            algorithm=self._algorithm,
            parameter_space = self._parameter_space,
            input_channels= input_channels, # telling SageMaker where the training data is located.
            estimator_config = self._estimator_config,
            objective_metric_name = self._objective_metric_name,
            objective_type=self._objective_type,
            max_jobs=self._max_jobs,
            max_parallel_jobs=self._max_parallel_jobs,
            job_name=self._job_name,
        '''
                

        self._tuner = self._sagemaker_manager.start_hyperparamter_tuning_job_no_hyper(
            algorithm=self._algorithm,
            input_channels= input_channels, # telling SageMaker where the training data is located.
            estimator_config = self._estimator_config,
            objective_metric_name = self._objective_metric_name,
            objective_type=self._objective_type,
            max_jobs=self._max_jobs,
            max_parallel_jobs=self._max_parallel_jobs,
            job_name=self._job_name,)


        return self


    def get_best_params(self): # Hyperparameters of the best trial
        return self._tuner.best_estimator().hyperparameters() 

    def get_best_score(self): # Metrics (e.g., best validation RMSE) from the best trial
        df = self._tuner.analytics().dataframe() 
        index = df["FinalObjectiveValue"].idxmin() # #give me index of smalelst valeue
        best_trial = df.loc[index] # returns entire row for that index
        return best_trial["FinalObjectiveValue"]

    def get_best_estimator(self): # SageMaker Estimator object for the best training job
        return self._tuner.best_estimator() 
       # best_estimator.hyperparameters()
       # best_estimator.deploy()
 
    def get_cv_results(self):  # DataFrame containing all hyperparameter tuning trials and their results
        return self._tuner.analytics().dataframe()

    '''
    def get_best_training_job_name(self):
        return self._tuner.best_training_job()
    '''