
from src_production_deployment.cloud.aws.sagemaker.ensemble.models.ensemble_result import EnsembleResult
from src_production_deployment.cloud.aws.sagemaker.ensemble.factory.ensemble_factory import EnsembleFactory
from src_production_deployment.cloud.aws.sagemaker.ensemble.generators.prediction_generator import PredictionGenerator
from src_production_deployment.cloud.aws.sagemaker.ensemble.config.ensemble_config import EnsembleConfig
from src_production_deployment.cloud.aws.sagemaker.ensemble.loaders.model_loader import ModelLoader
from src_production_deployment.evaluation.metrics_calculator import MetricsCalculator
import pandas as pd
import numpy as np
from src_production_deployment.mlflow.experiment_tracker import ExperimentTracker
from src_production_deployment.cloud.aws.sagemaker.ensemble.wrappers.weighted_average_wrapper import WeightedAverageWrapper
from src_production_deployment.training.training_utility.model_registry_utils import compare_and_register_model
from src_production_deployment.evaluation.metrics import calculate_rmsse
import time


class EnsemblePipeline:
    
    def __init__(self, model_loader: ModelLoader, prediction_generator: PredictionGenerator, evaluator : MetricsCalculator):

        self.model_loader = model_loader

        self.prediction_generator = prediction_generator

        self.evaluator = evaluator

    def run(self, X_val: pd.DataFrame, y_val: np.ndarray, config : EnsembleConfig, y_train = None) -> EnsembleResult:

        start = time.time()

        ensemble_model = self.model_loader.load()

        wrapper = WeightedAverageWrapper(ensemble_model = ensemble_model, weights = config.weights)

        prediction_set =  self.prediction_generator.generate(ensemble_model = ensemble_model, X = X_val)

        strategy = EnsembleFactory.create(config)
    
        predictions = strategy.aggregate(prediction_set)

        training_time = time.time() - start
        
        print(f"Training Time: {training_time:.2f} seconds")
        
        print("Model trained successfully")
        
        metrics = self.evaluator.calculate_metrics(y_val, predictions)

        rmsse = calculate_rmsse(y_train, y_true = y_val, y_pred = predictions)

        tracker = ExperimentTracker("Ensemble")

        with tracker.start_run(f"{strategy.name}_1.0"):

            tracker.log_params(config.to_mlflow_params())

            tracker.log_metrics({**metrics , "rmsse": rmsse, "training_time": training_time})

            wrapper = WeightedAverageWrapper(ensemble_model = ensemble_model, weights = config.weights)

            tracker.log_model(wrapper)

            compare_and_register_model(tracker = tracker, rmse = metrics["rmse"], rmsse = rmsse , model_name = f"DemandForecasting_{strategy.name}")

        return EnsembleResult(
            predictions=predictions,
            strategy=strategy.name,
            models=prediction_set.get_model_name()
        )


if __name__ == "__main__":

    loader = ModelLoader()

    prediction_generator = PredictionGenerator()

    evaluator = MetricsCalculator()

    pipeline = EnsemblePipeline(model_loader = loader , prediction_generator = prediction_generator, evaluator = evaluator)

    X_val = pd.read_parquet(r"artifacts/datasets/data_split/X_val.parquet")
    Y_val = pd.read_parquet(r"artifacts/datasets/data_split/Y_val.parquet")
    Y_train = pd.read_parquet(r"artifacts/datasets/data_split/Y_train.parquet")


    config = EnsembleConfig(stratergy = "simple_average")

    '''
    config = EnsembleConfig(stratergy="weighted_average",
                            weights={
                                    "DemandForecasting_XGBoost_RMSSE":  0.5,
                                    "DemandForecasting_LightGBM_RMSSE": 0.3,
                                    "DemandForecasting_CatBoost_RMSSE": 0.2
                            }
            )
    '''
    result = pipeline.run(X_val, Y_val, config, Y_train)

    print(result)
