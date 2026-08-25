from src_training.tuning.strategies.grid_search import GridsearchTuner
from src_training.tuning.strategies.random_search import RandomsearchTuner
from src_training.tuning.strategies.optuna.optuna_search import OptunaTuner
from src_training.ensemble.tuning_enum import  TuningStrategy
from src_training.tuning.strategies.ray_optuna_stratergy import RayOptunaStrategy
from src_training.tuning.strategies.sagemaker_strategy import SageMakerStratergy

class TuningstratergyFactory:

    @staticmethod
    def create(stratergy,estimator,parameter_space,algorithm, tuning_config = None,):
        
        if stratergy == TuningStrategy.GRID_SEARCH:
            return GridsearchTuner(estimator = estimator, parameter_space = parameter_space)

        elif stratergy == TuningStrategy.RANDOM_SEARCH:
            return RandomsearchTuner(estimator = estimator, parameter_space = parameter_space)
        
        elif stratergy == TuningStrategy.OPTUNA:
            return OptunaTuner(estimator = estimator, parameter_space = parameter_space, algorithm = algorithm)
        
        elif stratergy == TuningStrategy.RAY_OPTUNA:
            return RayOptunaStrategy(estimator = estimator, parameter_space = parameter_space, algorithm = algorithm)

        elif stratergy == TuningStrategy.SAGEMAKER:

            if tuning_config is None:
                   raise ValueError("tuning_config is required for SageMaker strategy.")
            
            return SageMakerStratergy(
                                        estimator = estimator,
                                        parameter_space= parameter_space,
                                        algorithm = algorithm,
                                        sagemaker_manager = tuning_config.sagemaker_manager,
                                        artifact_manager = tuning_config.artifact_manager,
                                        estimator_config = tuning_config.estimator_config, 
                                        dataset_name=tuning_config.dataset_name,
                                        objective_metric_name=tuning_config.objective_metric_name,
                                        objective_type=tuning_config.objective_type,
                                        max_jobs=tuning_config.max_jobs,
                                        max_parallel_jobs=tuning_config.max_parallel_jobs,
                                        job_name=tuning_config.job_name,
                                    )
        
        raise ValueError(f'{stratergy} is not supported')
         
        
             