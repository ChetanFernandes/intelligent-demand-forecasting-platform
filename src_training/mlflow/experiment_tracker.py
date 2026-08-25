import mlflow
import mlflow.sklearn
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

class ExperimentTracker:
    """
    Wrapper class for MLflow experiment tracking.
    """

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment(experiment_name)

    def start_run(self, run_name: str):
        return mlflow.start_run(run_name=run_name)

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict):
        mlflow.log_metrics(metrics)
        print("Metrics logged successfully.")

    def log_tags(self, tags: dict):
        mlflow.set_tags(tags)

    def log_model(self, model, artifact_path="model",serialization_format="cloudpickle"):

        if isinstance(model, LGBMRegressor):
            mlflow.lightgbm.log_model(
                lgb_model=model,
                name=artifact_path
            )

        elif isinstance(model, XGBRegressor):
            mlflow.xgboost.log_model(
                xgb_model=model,
                name=artifact_path
            )

        elif isinstance(model, CatBoostRegressor):
            mlflow.catboost.log_model(
                cb_model=model,
                name=artifact_path
            )

        else:
            mlflow.sklearn.log_model(
                sk_model=model,
                name=artifact_path,
                serialization_format=serialization_format
            )

    def log_artifact(self,artifact_path:str):
        mlflow.log_artifact(artifact_path)

    def log_artifacts(self, artifact_directory: str):
        mlflow.log_artifacts(artifact_directory)
    
    def register_model(self,model_uri:str,model_name:str):
        mlflow.register_model(model_uri=model_uri, name=model_name)

    def end_run(self):
        mlflow.end_run()

        
