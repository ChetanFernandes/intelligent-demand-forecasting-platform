from src_training.ensemble.constant.constants import ENSEMBLE_MODELS, MODEL_VERSIONS
from registry.mlflow_registry import ModelRegistry
#from pathlib import Path
#import yaml
from src_training.ensemble.models.ensemble_model import EnsembleModel
from typing import Any
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import inspect

class EstimatorLoader:
    def __init__(self):
        self.registry = ModelRegistry()


    def _convert_value(self,value:Any) -> Any:

        if value == "None":
            return None

        if value == "True":
            return True

        if value == "False":
            return False

        if value == "nan":
            return float("nan")

        try:
            if "." not in str(value):
                return int(value)
        except (ValueError, TypeError):
            pass # If conversion fails, Python jumps to the except block and continues to the next conversion.

        try:
            return float(value)
        except (ValueError, TypeError):
            return value

    def _filter_params(self,estimator_class,params:dict) -> dict:

            # XGBoost: use get_params()
        if estimator_class == XGBRegressor:
            valid_params = XGBRegressor().get_params().keys()

        # LightGBM & CatBoost: use constructor signature
        else:
            valid_params = inspect.signature(estimator_class.__init__).parameters.keys()
        
        filtered = {}

        for key, value in params.items():

             # Skip unsupported parameter
            if key not in valid_params:
                continue # immediately skips the rest of the current iteration and goes back to the top of the loop for the next item.

            # Skip parameters you don't want
            if key in ["missing", "early_stopping_rounds" , "use_best_model","sample_size"]:
                continue 

        
            value = self._convert_value(value)

            if value is None:
                continue

            filtered[key] = value

        return filtered

    def load(self) -> EnsembleModel:
        models = {}
        testing = {}
        estimator_mapping = {
        "DemandForecasting_XGBoost_RMSSE": XGBRegressor,
        "DemandForecasting_LightGBM_RMSSE": LGBMRegressor,
        "DemandForecasting_CatBoost_RMSSE": CatBoostRegressor,
    }     
        #path = Path("src/ensemble/config/params.yaml")
        #path.parent.mkdir(parents = True, exist_ok = True)
          
        for model_name in ENSEMBLE_MODELS:

            version = MODEL_VERSIONS[model_name]

            details  = self.registry.get_model_details(model_name,version)

            estimator_class = estimator_mapping[model_name]

            filtered_params = self._filter_params(estimator_class, details["params"])
   
            testing[model_name] = filtered_params

            if estimator_class == CatBoostRegressor:

                if "random_state" in filtered_params:

                    filtered_params["random_seed"] = filtered_params.pop("random_state") 

                filtered_params.setdefault("verbose", False)

            models[model_name] = estimator_class(**filtered_params)

    
        #with open(path,"w") as f:
            #yaml.safe_dump(testing, f, sort_keys=False)
        print(models)
        return EnsembleModel(models = models)


  
if __name__ == "__main__":
    loader = EstimatorLoader()
    loader.load()








