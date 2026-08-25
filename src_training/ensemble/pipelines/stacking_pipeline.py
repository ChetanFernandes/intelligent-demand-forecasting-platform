
from src_training.ensemble.generators.prediction_generator import PredictionGenerator
from src_training.ensemble.generators.oof_prediction_generator import OOFPredictionGenerator
from src_training.ensemble.models.ensemble_result import EnsembleResult
from src_training.ensemble.factory.ensemble_factory import EnsembleFactory
from src_training.ensemble.config.ensemble_config import EnsembleConfig
#from src.evaluation.metrics_calculator import MetricsCalculator
import pandas as pd
import numpy as np
#from src.training.training_utility.model_registry_utils import compare_and_register_model
#from src.evaluation.metrics import calculate_rmsse
#from src.mlflow.experiment_tracker import ExperimentTracker
from src_training.ensemble.wrappers.stacking_wrapper import StackingWrapper
from sklearn.linear_model import Ridge
import time, os
from src_training.ensemble.config.params_loader import EstimatorLoader
import joblib
from sklearn.metrics import root_mean_squared_error

class StackingPipeline:

    def __init__(self, loader : EstimatorLoader, prediction_generator: PredictionGenerator, oof_prediction_generator: OOFPredictionGenerator, 
                 evaluator):

        self.model_loader = loader
        self.prediction_generator = prediction_generator
        self.oof_prediction_generator = oof_prediction_generator
        self.evaluator = evaluator

    def run(self, X_train: pd.DataFrame, y_train: np.ndarray, X_val: pd.DataFrame, y_val:pd.DataFrame, config: EnsembleConfig) -> EnsembleResult:

        assert (X_train.index == y_train.index).all(), \
        "X_train and y_train indices do not match."
    
        start_time = time.time()

        # trained_model_object = self.model_loader.load() # These models are already trained 
        #tracker = ExperimentTracker("Ensemble")

        #with tracker.start_run(f"stacking_1.0"):
            
        ensemble_model = self.model_loader.load() 
        
        train_prediction_set = self.oof_prediction_generator.generate(ensemble_model = ensemble_model , X = X_train, y = y_train)

        strategy = EnsembleFactory.create(config)

        strategy.fit(train_prediction_set,y_train) # Train the meta-model using out-of-fold predictions

        training_time = time.time() - start_time

        # Validation
        validation_prediction_set = self.prediction_generator.generate(ensemble_model = ensemble_model, X = X_val)

        predictions = strategy.predict(validation_prediction_set).ravel()

        #metrics = self.evaluator.calculate_metrics(y_val, predictions)
        
        #rmsse = calculate_rmsse(y_train, y_true = y_val, y_pred = predictions)

        #tracker.log_params(config.to_mlflow_params())

        rmse = root_mean_squared_error(y_val, predictions)

        print(f"validation:rmse={rmse}")

        #tracker.log_metrics({**metrics , "rmsse": rmsse, "training_time": training_time})

        wrapper = StackingWrapper(ensemble_model = ensemble_model, meta_model = strategy.model)

        #tracker.log_model(wrapper)

        #compare_and_register_model(tracker = tracker, rmse = metrics["rmse"], rmsse = rmsse , model_name = f"DemandForecasting_{strategy.name}")
        
        model_path = os.path.join(model_dir, "model.joblib")

        joblib.dump(wrapper, model_path)
        
        return EnsembleResult(
                    predictions=predictions,
                    strategy=strategy.name,
                    models=validation_prediction_set.get_model_name()
                              )
    
if __name__ == "__main__":

    trained_loader = EstimatorLoader()
    prediction_generator = PredictionGenerator()
    oof_prediction_generator = OOFPredictionGenerator()
    #evaluator = MetricsCalculator()

    stacking_pipeline = StackingPipeline( loader = trained_loader , prediction_generator = prediction_generator,
                                oof_prediction_generator = oof_prediction_generator , evaluator = None)

    train_data_dir = os.environ["SM_CHANNEL_TRAIN"]
    model_dir = os.environ["SM_MODEL_DIR"]

    X_train = pd.read_parquet(os.path.join(train_data_dir, "X_train.parquet"))
    y_train = pd.read_parquet(os.path.join(train_data_dir, "y_train.parquet"))
    X_val = pd.read_parquet(os.path.join(train_data_dir, "x_val.parquet"))
    y_val = pd.read_parquet(os.path.join(train_data_dir, "y_val.parquet"))



    #X_train = pd.read_parquet(r"artifacts/datasets/data_split/X_train.parquet")
    #y_train = pd.read_parquet(r"artifacts/datasets/data_split/Y_train.parquet")
    #X_val = pd.read_parquet(r"artifacts/datasets/data_split/X_val.parquet")
    #y_val = pd.read_parquet(r"artifacts/datasets/data_split/Y_val.parquet")

    print(X_train.shape)
    print(y_train.shape)
    

    #X_train_small = X_train.sample(2500000, random_state=42)
    #y_train_small = y_train.loc[X_train_small.index]

    #assert (X_train.index == y_train.index).all()


    #print(X_train_small.shape)
    #print(y_train_small.shape)
    ridge = Ridge(alpha=1.0)

    config = EnsembleConfig(stratergy = "stacking", meta_model = ridge)

    results = stacking_pipeline.run(X_train,y_train,X_val,y_val, config)

    print(results)
  