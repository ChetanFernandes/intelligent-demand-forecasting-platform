import mlflow
class mlflow_aws:
    
    def __init__(self, experiment_name:str) -> None :
        mlflow.set_tracking_uri("arn:aws:sagemaker:us-east-1:135053048192:mlflow-app/app-K53I5ZJMEUHZ")
        #self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)

    
    def start_run(self, run_name=None):
        return mlflow.start_run(run_name=run_name)

    def log_metric(self, key: str, value: float):
         mlflow.log_metric(key, value)

    def log_metrics(self,metric:dict):
        mlflow.log_metrics(metric)
        print("Metrics logged successfully.")

    def log_model(self, model, artifact_path="model",serialization_format="cloudpickle"):
        mlflow.sklearn.log_model(
                        sk_model = model,
                        artifact_path = artifact_path,
                        serialization_format=serialization_format
                    )
    def register_model(self,model_name:str):
        run_id = mlflow.active_run().info.run_id
        
        mlflow.register_model(model_uri=f"runs:/{run_id}/model", name = model_name)
    

'''
client = mlflow.MlflowClient()

for exp in client.search_experiments():
    print(exp.name)

mlflow.set_experiment("AWS_Test")

with mlflow.start_run(run_name="First_Run"):
    mlflow.log_param("learning_rate", 0.1)
    mlflow.log_metric("rmse", 1.95)

print("Success!")


client = mlflow.MlflowClient()

for exp in client.search_experiments():
    print(exp.name)
'''