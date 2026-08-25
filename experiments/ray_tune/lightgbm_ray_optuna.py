from ray import tune
from ray.tune.search.optuna import OptunaSearch
from lightgbm import LGBMRegressor
from src_training.tuning.strategies.ray_optuna_stratergy import RayOptunaStrategy
from src_training.tuning.parameter import LIGHTGBM_OPTUNA_PARAMETER_SPACE

trainable = LGBMRegressor()

straterhy = RayOptunaStrategy(trainable = trainable, param_space = LIGHTGBM_OPTUNA_PARAMETER_SPACE, metric="rmse", mode="min", num_samples=10,  )







'''
What is ray.tune?

This is the ML Experimentation department.

It knows about:

Trials
Search Spaces
Hyperparameter Optimization
Search Algorithms
Schedulers
Metrics
'''


