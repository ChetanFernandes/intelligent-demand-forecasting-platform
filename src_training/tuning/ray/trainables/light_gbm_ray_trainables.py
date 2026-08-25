from ray import tune
from src_training.tuning.strategies.optuna.algorithms_engines.lightgbm.light_gbm_training import LightGBMTrainingEngine
from src_training.tuning.progress.ray_progress_reporter import RayProgressReporter


def light_gbm_trainable(config,estimator,X_train,y_train,n_splits):
    ''' Receive:
            - config
            - estimator
            - X_train
            - y_train
            - n_splits
                ↓
                Create TrainingEngine
                ↓
                Train
                ↓
                Report metrics
    '''
    print(config)
    engine = LightGBMTrainingEngine(estimator=estimator,X_train=X_train,y_train=y_train,n_splits=n_splits)
    # This means every trial creates a brand new LightGBMTrainingEngine.
    # This is intentional. Each trial should be completely independent, with no state carried over from previous trials.
    
    progress_reporter = RayProgressReporter()

    engine.evaluate(params=config, progress_reporter = progress_reporter)
    
  
