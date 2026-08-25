from src_training.registry.mlflow_registry import ModelRegistry

registry = ModelRegistry()

latest_model = registry.get_latest_model_version("DemandForecasting_LightGBM")

run_id = registry.get_run_id("DemandForecasting_LightGBM")

metrics = registry.get_run_metrics(run_id)

print(latest_model)

print(run_id)

print(metrics)