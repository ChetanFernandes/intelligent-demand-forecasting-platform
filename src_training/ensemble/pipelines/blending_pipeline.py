from src_training.ensemble.models.ensemble_result import EnsembleResult
from src_training.ensemble.generators.prediction_generator import PredictionGenerator
from src_training.ensemble.factory.ensemble_factory import EnsembleFactory
from src_training.ensemble.config.ensemble_config import EnsembleConfig
import numpy as np
import pandas as pd
from src_training.ensemble.loaders.model_loader import ModelLoader
from src_training.ensemble.data.blending_splitter import BlendingSplitter
from src_training.evaluation.metrics_calculator import MetricsCalculator
from src_production_deployment.training.training_utility.model_registry_utils import compare_and_register_model
from src_training.evaluation.metrics import calculate_rmsse
from src_production_deployment.mlflow.experiment_tracker import ExperimentTracker
from src_training.ensemble.wrappers.blended_wrapper import BlendedWrapper
from sklearn.linear_model import Ridge


import time

class BlendingPipeline:

    def __init__(self, model_loader : ModelLoader , prediction_generator: PredictionGenerator,  blending_splitter: BlendingSplitter, evaluator = MetricsCalculator):

        self.model_loader = model_loader
        self.prediction_generator = prediction_generator
        self.blending_splitter = blending_splitter
        self.evaluator = evaluator
    
    def run(self, X_val: pd.DataFrame, y_val: np.ndarray, config: EnsembleConfig, Y_train = None) -> EnsembleResult:

        start_time = time.time()

        tracker = ExperimentTracker("Ensemble")

        with tracker.start_run(f"Blending_1.0"):

            X_blend_train, X_blend_validation, y_blend_train, y_blend_validation = self.blending_splitter.split(X_val,y_val)

            ensemble_model = self.model_loader.load()

            # Generate prediction by base model
            
            blend_train_prediction_set  = self.prediction_generator.generate(ensemble_model = ensemble_model, X = X_blend_train)

            strategy = EnsembleFactory.create(config)

            # Train the meta_model by using prediction generatd by meta model (above step)

            strategy.fit(blend_train_prediction_set, y_blend_train) # training meta model

            training_time = time.time() - start_time

            # Validation steps
            # Generate prediction by base model

            blend_validation_prediction_set = self.prediction_generator.generate(ensemble_model = ensemble_model, X = X_blend_validation)

            # Prediction done by meta model
            
            predictions = strategy.predict(blend_validation_prediction_set).ravel() # to flatten the shape from (n_samples, 1) to (n_samples,)

            metrics = self.evaluator.calculate_metrics(y_blend_validation, predictions)

            rmsse = calculate_rmsse(Y_train, y_true = y_blend_validation, y_pred = predictions)

            
            tracker.log_params(config.to_mlflow_params())

            tracker.log_metrics({**metrics , "rmsse": rmsse, "training_time": training_time})

            wrapper = BlendedWrapper(ensemble_model = ensemble_model, meta_model = strategy.model)

            tracker.log_model(wrapper)

            compare_and_register_model(tracker = tracker, rmse = metrics["rmse"], rmsse = rmsse , model_name = f"DemandForecasting_{strategy.name}")
            
        
            return EnsembleResult(
                predictions  = predictions,
                strategy = strategy.name,
                models = blend_validation_prediction_set.get_model_name()
            )

if __name__ == "__main__":

    loader = ModelLoader()
    generator = PredictionGenerator()
    spliter = BlendingSplitter()
    evalutaor = MetricsCalculator()



    ridge = Ridge(alpha=1.0)

    config = EnsembleConfig(stratergy="blending", meta_model=ridge)

    blend_pipeline = BlendingPipeline(model_loader = loader, prediction_generator = generator, blending_splitter = spliter, evaluator = MetricsCalculator)

    X_val = pd.read_parquet(r"artifacts/datasets/data_split/X_val.parquet")
    Y_val = pd.read_parquet(r"artifacts/datasets/data_split/Y_val.parquet")
    Y_train = pd.read_parquet(r"artifacts/datasets/data_split/Y_train.parquet")

    config = EnsembleConfig(stratergy = "blending", meta_model = ridge)
    results = blend_pipeline.run(X_val,Y_val,config,Y_train)
    print(results)






   

'''
The Real Blending Workflow

This is what we'll implement next:

Original Dataset
        │
        ▼
Train / Blend / Test
Train set
    Train XGBoost
    Train LightGBM
    Train CatBoost
Blend set
    Generate predictions from the trained base models.
    Train the meta-model using those predictions.
Test set
    Generate predictions from the base models.
    Pass them to the trained meta-model.
    Evaluate the final ensemble.

This is the real blending pipeline.
'''