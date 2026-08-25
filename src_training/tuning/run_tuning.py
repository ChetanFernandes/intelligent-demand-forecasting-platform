
from src_training.training.data.data_loader import load_data_hyper
from src_training.encoding.encoder_processor import preprocess_data_hyper_target, preprocess_data_hyper_native
from lightgbm import LGBMRegressor
from src_training.tuning.tuning_pipeline import TuningPipeline
from src_training.cloud.aws.sage_parameter import LIGHTGBM_SAGE_PARAMETER_SPACE, XGBOOST_SAGE_PARAMETER_SPACE, CATBOOST_SAGE_PARAMETER_SPACE
from src_training.tuning.parameter import LIGHTGBM_PARAMETER_GRID, LIGHTGBM_PARAMETER_RANDOM ,CATBOOST_PARAMETER_RANDOM 
from src_training.tuning.strategies.optuna.optuna_parameters import XGBOOST_OPTUNA_PARAMETER_SPACE, LIGHTGBM_OPTUNA_PARAMETER_SPACE,CATBOOST_OPTUNA_PARAMETER_SPACE
from src_training.tuning.tuning_report import TuningReporter
from src_training.ensemble.tuning_enum import Algorithm, TuningStrategy
from src_training.config.tuning_config_factory import TuningConfigFactory
from src_training.training.training_utility.mlflow_utils import log_experiment_hyper
from src_training.mlflow.experiment_tracker import ExperimentTracker
from catboost import CatBoostRegressor
from xgboost import XGBRegressor


def main():

    X_train, Y_train = load_data_hyper()

    print(X_train.shape)

    X_train_sample, y_train_sample  = preprocess_data_hyper_target(X_train, Y_train)

    print(X_train_sample.shape, y_train_sample.shape)

    print((X_train_sample.index == y_train_sample.index).all())


    # use only when youre calling catregresor

    #estimator = LGBMRegressor()

    #estimator = XGBRegressor()

    estimator = CatBoostRegressor()
  
    strategy = TuningStrategy.SAGEMAKER
    
    tuning_config = TuningConfigFactory.create(strategy)    

    tracker = ExperimentTracker("Ensemble_SageMakwer")

    with tracker.start_run(f"stacking_Sage"):

      tuning_pipeline = TuningPipeline(estimator = None, parameter_space = None,  
                                       algorithm = Algorithm.ENSEMBLE, stratergy = strategy, tuning_config = tuning_config, 
                                      )

      X_train_sample, y_train_sample  = None, None

      best_params, best_score = tuning_pipeline.run(X_train_sample, y_train_sample, job_name = tuning_config.job_name)

  
      log_experiment_hyper(tracker = tracker, best_params = best_params, best_rmse = best_score, stratergy = TuningStrategy.OPTUNA.value)

      report = TuningReporter(best_params, best_score)

      report.display()
     
    
    
if __name__ == '__main__':
    main()

'''
run_tuning.py
      │
      ▼
strategy="grid_search"
      │
      ▼
TuningPipeline
      │
      ▼
TuningStrategyFactory
      │
      ▼
GridSearchTuner
'''

'''
main()
   │
   ├── SageMakerEstimatorConfig
   │
   └── SageMakerTuningConfig
            │
            ▼
TuningStrategyFactory
            │
            ▼
SageMakerStrategy
            │
            ▼
SageMakerManager
            │
            ▼
SageMakerEstimatorFactory
            │
            ▼
SKLearn Estimator
'''