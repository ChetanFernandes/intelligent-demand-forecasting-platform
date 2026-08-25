import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")

client = mlflow.MlflowClient()

run = client.get_run("8e2e23d3d091472d9d26ef2ae8adb17d")

print("Artifact URI:", run.info.artifact_uri)

'''
version = client.get_model_version(
    name="DemandForecasting_Blending",
    version="1"
)


print("Run ID:", version.run_id)
print("Source:", version.source)

'''