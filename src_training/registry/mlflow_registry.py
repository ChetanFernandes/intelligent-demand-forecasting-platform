from mlflow import MlflowClient
import mlflow

class ModelRegistry:
    def __init__(self):
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        self.client = MlflowClient()


    def get_latest_model_version(self,model_name):
        latest_version = self.client.get_latest_versions(model_name)
        if not latest_version:
            return None
        return latest_version[-1]
    
    def get_run_id(self,model_name):
        latest_model = self.get_latest_model_version(model_name)
        if latest_model is None:
            return None

        return latest_model.run_id
    
    def get_run_metrics(self,run_id):
        run = self.client.get_run(run_id)
        return run.data.metrics
    
    def get_model_details(self, model_name: str, version: int | str = "latest"):

        if version == "latest":
            model_version = self.get_latest_model_version(model_name)
        else:
            model_version = self.client.get_model_version(
                name=model_name,
                version=str(version)
            )

        if model_version is None:
            return None

        run = self.client.get_run(model_version.run_id)

        return {
            "model_name": model_name,
            "version": model_version.version,
            "run_id": model_version.run_id,
            "metrics": run.data.metrics,
            "params": run.data.params,
            "tags": run.data.tags,
        }

    def get_model_uri(self, model_name: str, version: int | str = "latest"):

        if version == "latest":
            latest = self.get_latest_model_version(model_name)

            if latest is None:
                return None

            return f"models:/{model_name}/{latest.version}"

        return f"models:/{model_name}/{version}"