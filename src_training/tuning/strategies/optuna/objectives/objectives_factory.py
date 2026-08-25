from src_training.ensemble.tuning_enum import Algorithm
from src_training.tuning.strategies.optuna.algorithms_engines.lightgbm.lightgbm_objectives import LightGBMObjective
from src_training.tuning.strategies.optuna.algorithms_engines.xgboost.xg_boost_objective import XGBoostObjective
from src_training.tuning.strategies.optuna.algorithms_engines.catboost.cat_boost_objective import CatBoostObjective


class ObjectiveFactory:

    @staticmethod
    def create(algorithm, estimator, parameter_space, X_train, y_train, n_splits):

        if algorithm == Algorithm.LIGHTGBM:

            return LightGBMObjective(estimator=estimator, parameter_space = parameter_space, X_train=X_train, y_train=y_train, n_splits = n_splits)

        elif algorithm == Algorithm.XGBOOST:

            return XGBoostObjective(estimator=estimator, parameter_space = parameter_space, X_train=X_train, y_train=y_train, n_splits = n_splits)

        elif algorithm == Algorithm.CATBOOST:
        
            return CatBoostObjective(estimator=estimator, parameter_space = parameter_space, X_train=X_train, y_train=y_train, n_splits = n_splits)
                    
        

        raise ValueError(
            f"Unsupported algorithm: {algorithm}"
        )