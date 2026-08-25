from pathlib import Path
import yaml

from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

from src_training.ensemble.models.ensemble_model import EnsembleModel
from src_training.ensemble.constant.constants import ENSEMBLE_MODELS


class EstimatorLoader_yaml:

    def __init__(self, yaml_path: str = "ensemble/config/params.yaml"):
        self.yaml_path = yaml_path

    def load(self) -> EnsembleModel:

        with open(self.yaml_path, "r") as f:
            all_params = yaml.safe_load(f)

        estimator_mapping = {
            "DemandForecasting_XGBoost_RMSSE": XGBRegressor,
            "DemandForecasting_LightGBM_RMSSE": LGBMRegressor,
            "DemandForecasting_CatBoost_RMSSE": CatBoostRegressor,
        }

        models = {}

        for model_name in ENSEMBLE_MODELS:

            estimator_class = estimator_mapping[model_name]

            params = all_params.get(model_name, {}).copy()

            # XGBoost
            if estimator_class == XGBRegressor:
                params.pop("missing", None)
                params.pop("early_stopping_rounds", None)

            # CatBoost
            elif estimator_class == CatBoostRegressor:

                params.pop("use_best_model", None)
                params.pop("early_stopping_rounds", None)

                if "random_state" in params:
                    params["random_seed"] = params.pop("random_state")

                params.setdefault("verbose", False)

            models[model_name] = estimator_class(**params)

        return EnsembleModel(models=models)


if __name__ == "__main__":

    loader = EstimatorLoader_yaml()

    ensemble_model = loader.load()

    for name, model in ensemble_model.models.items():
        print(f"{name}")
        print(model)