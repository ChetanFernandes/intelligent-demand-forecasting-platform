from enum import Enum

class Algorithm(Enum):

    LIGHTGBM = "lightgbm"

    XGBOOST = "xgboost"

    CATBOOST = "catboost"

    ENSEMBLE = "ensemble"


class TuningStrategy(Enum):

    GRID_SEARCH = "grid_search"

    RANDOM_SEARCH = "random_search"

    OPTUNA = "optuna"

    SAGEMAKER = "sagemaker"

    RAY_OPTUNA = "ray_optuna"
