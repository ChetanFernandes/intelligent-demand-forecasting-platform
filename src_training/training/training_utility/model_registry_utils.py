import mlflow
from src_production_deployment.registry.mlflow_registry import ModelRegistry
from src_production_deployment.registry.model_evaluator import ModelEvaluator
registry = ModelRegistry()
evaluator = ModelEvaluator()
from logger.logging import setup_logging
log = setup_logging()



def compare_and_register_model(tracker, rmse, rmsse, model_name):

    try:
        log.info(f"Inside compare model")
        run_id = registry.get_run_id(model_name)

        metrics = registry.get_run_metrics(run_id)

        best_rmse = metrics["rmse"]
        best_rmsse = metrics["rmsse"]

        print(f"Registered RMSE : {best_rmse:.4f}")
        print(f"Current RMSE    : {rmse:.4f}")

        print(f"Registered RMSSE : {best_rmsse:.4f}")
        print(f"Current RMSSE    : {rmsse:.4f}")


        if evaluator.is_better(rmse, rmsse, best_rmse, best_rmsse):

            print("Better model found. Registering...")

            run_id = mlflow.active_run().info.run_id

            tracker.register_model(
                model_uri=f"runs:/{run_id}/model",
                model_name=model_name
            )

            print("Model registered successfully.")

        else:

            print("Current registered model is still better.")

    except Exception as e:
        log.exception(f"Exception occured  -{str(e)}")
        print("No registered model found.")
        print("Registering first model...")

        run_id = mlflow.active_run().info.run_id

        tracker.register_model(
            model_uri=f"runs:/{run_id}/model",
            model_name=model_name
        )
