from src_training.training.models.XGboost.trainer import XGBoostTrainer
from configs.model_params import XGBOOST_BEST_PARAMS
from configs.project_config import FEATURE_IMPORTANCE_PATH,EXPERIMENT_NAME
from src_training.training.data.data_loader import load_data
from src_training.encoding.encoder_processor import preprocess_data_test_target, preprocess_data_test_native
from src_training.training.training_utility.training_utils import train_and_evaluate
from src_training.training.training_utility.mlflow_utils import log_experiment
from src_training.mlflow.experiment_tracker import ExperimentTracker
from src_training.training.training_utility.model_registry_utils import compare_and_register_model
from src_training.tuning.hyperparameter_manager import HyperparameterManager
from src_production_deployment.cloud.aws.sagemaker.tuning_enum import Algorithm, TuningStrategy

def main():
    
    print("XGBoost Training Pipeline Started")

    X_train, y_train, X_val, Y_val = load_data()

    print(X_train.dtypes)
    
    print(X_train.shape, y_train.shape, X_val.shape, Y_val.shape)
    
    X_train,  X_val = preprocess_data_test_target(X_train,X_val,y_train)
    
    print(X_train.shape, y_train.shape, X_val.shape, Y_val.shape)

    trainer = XGBoostTrainer()

    best_params = HyperparameterManager.load_best_parameters(algorithm = Algorithm.XGBOOST.value, stratergy = TuningStrategy.OPTUNA.value)

    tracker = ExperimentTracker(EXPERIMENT_NAME)

    with tracker.start_run(f"{Algorithm.XGBOOST.value}_Target_Encoding_2"):

        model, mae, rmse, mape, smape, wape, rmsse, training_time= train_and_evaluate(trainer, X_train,y_train, X_val,Y_val, best_params)

        importance_df = trainer.get_feature_importance(model, X_train)

        log_experiment(tracker=tracker, model=model, mae=mae, rmse=rmse, mape = mape, smape = smape, wape = wape, rmsse = rmsse, training_time=training_time, importance_df=importance_df,
                            feature_importance_path=FEATURE_IMPORTANCE_PATH, X_train_sample=X_train, 
                            alogorthm_name_tag = Algorithm.XGBOOST.value)
            
        print("All parameters logged to mlflow successfully")

        compare_and_register_model(tracker=tracker, rmse=rmse, rmsse = rmsse , model_name = "DemandForecasting_XGBoost_RMSSE")

if __name__ == "__main__":
    main()