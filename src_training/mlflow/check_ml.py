import mlflow



mlflow.set_tracking_uri("sqlite:///mlflow.db")

print("Tracking URI:", mlflow.get_tracking_uri())

client = mlflow.MlflowClient()

print("\nExperiments:")
for exp in client.search_experiments():
    print(f"ID: {exp.experiment_id}, Name: {exp.name}")