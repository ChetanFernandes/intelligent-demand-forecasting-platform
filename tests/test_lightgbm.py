from src_training.training.models.LightGBM.trainer import LightGBMTrainer
from src_training.encoding.categoral_encoder import CategoricalEncoder
import pandas as pd
import time
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from src_training.mlflow.experiment_tracker import ExperimentTracker
from src_training.registry.model_evaluator import ModelEvaluator
from src_training.registry.mlflow_registry import ModelRegistry
import mlflow
from configs.project_config import MODEL_NAME
from configs.model_params import LIGHTGBM_BEST_PARAMS

trainer = LightGBMTrainer()
encoder = CategoricalEncoder()
evaluator = ModelEvaluator()
registry = ModelRegistry()

X_train = pd.read_parquet(r"artifacts\datasets\X_train.parquet")
Y_train = pd.read_parquet(r"artifacts\datasets\Y_train.parquet")

X_val = pd.read_parquet(r"artifacts\datasets\X_val.parquet")
Y_val = pd.read_parquet(r"artifacts\datasets\Y_val.parquet")


X_train = encoder.transform(X_train)
X_val = encoder.transform(X_val)

X_train_sample = X_train.sample(n=500000,random_state=54)
y_train_sample = Y_train.loc[X_train_sample.index]

print((X_train_sample.index == y_train_sample.index).all())

tracker = ExperimentTracker("Demand Forecasting")

with tracker.start_run("LightGBM_Baseline_v1"):

    start = time.time()
   
    '''
    model_params = {
                   'colsample_bytree':0.8,
                   'importance_type':"gain",
                   'learning_rate':0.05,
                   'max_depth':-1,
                   'min_child_samples':20,
                   'min_child_weight':0.001,
                   'min_split_gain':0.5,
                   'num_leaves':25,
                   'n_estimators':110,
                   'n_jobs':-1,
                   'objective':'regression',
                   'random_state':42,
                   'reg_alpha':0.0,
                   'reg_lambda':0.0,
                   'sample_size': 500000,
                   'subsample':1.0,
                   'subsample_for_bin':200000,
                   'subsample_freq':4,
                   }
    '''

    model = trainer.train(X_train_sample,y_train_sample,**LIGHTGBM_BEST_PARAMS)

    print("\n Model Parameters:")

    print(model.get_params())

    tracker.log_params(model.get_params())

    tracker.log_params({"sample_size": len(X_train_sample)})

    training_time = time.time() - start

    print(f"Training Time: {training_time:.2f} seconds")

    print("Model trained successfully")

# Prediction

    predictions = model.predict(X_val)

    print(f"Prediction Shape: {predictions.shape}")

    mae = mean_absolute_error(Y_val,predictions)

    rmse = root_mean_squared_error(Y_val,predictions)

    run_id = registry.get_run_id(MODEL_NAME)
    metrics = registry.get_run_metrics(run_id)
    best_rmse = metrics["rmse"]

    print(f"Current Registered RMSE : {best_rmse:.4f}")
    print(f"Current Model RMSE      : {rmse:.4f}")

    if evaluator.is_better(rmse, best_rmse):

        run_id = mlflow.active_run().info.run_id

        tracker.register_model(
            model_uri=f"runs:/{run_id}/model",
            model_name=MODEL_NAME)
        
        print("✅ Model registered successfully.")
    else:
        print("❌ Model is not better than the current best.")


    print(f"MAE : {mae}")
    print(f"RMSE: {rmse}")

    tracker.log_metrics({"mae": mae, "rmse": rmse, "training_time":training_time})

    tracker.log_tags({
                        "algorithm": "LightGBM",
                        "dataset": "M5 Forecasting",
                        "model_type": "Baseline",
                    })

    tracker.log_model(model)

    print("Model logged to MLflow successfully.")

    #Path("artifacts/models").mkdir(parents=True,exist_ok=True)

    #joblib.dump(model,"artifacts/models/lightgbm_baseline.pkl")

    #print("Model saved successfully")

    importance_df = trainer.get_feature_importance(model, X_train_sample)

    feature_importance_path = "artifacts/feature_importance.csv"

    importance_df.to_csv(feature_importance_path, index=False)

    tracker.log_artifact(feature_importance_path)

    print("Feature importance logged to MLflow successfully.")

    print(importance_df.head(20))
