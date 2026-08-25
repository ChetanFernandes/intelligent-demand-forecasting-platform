from dataclasses import dataclass
from src_training.cloud.aws.config.base_tuning_config import BaseTuningConfig
from src_production_deployment.production_deployment.artifacts_manager import ArtifactManager
from src_training.cloud.aws.sagemaker.sagemaker_manager import SageMakerManager
from src_training.cloud.aws.sagemaker.estimator_config import SageMakerEstimatorConfig

@dataclass
class SageMakerTuningConfig(BaseTuningConfig):
    dataset_name : str
    objective_metric_name : str
    objective_type:str
    max_jobs:int
    max_parallel_jobs:int
    job_name:str
    sagemaker_manager: SageMakerManager
    artifact_manager: ArtifactManager
    estimator_config: SageMakerEstimatorConfig

