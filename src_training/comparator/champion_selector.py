from mlflow import MlflowClient

class ChampionSelector:

    def __init__(self):
        self.client = MlflowClient()

    def register_champion(self,champion):
        model_uri = f"runs:/{champion['run_id']}/model"
        self.tracker.register_model(model_uri = model_uri, model_name = "DemandForecasting_Champion")

        print(f"Champion Model Registered : {champion['model_name']}")