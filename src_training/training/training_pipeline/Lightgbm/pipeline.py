from src_training.training.models.LightGBM.trainer import LightGBMTrainer
from src_training.encoding.encoder_processor import preprocess_data__test_target
from src_training.training.training_utility.training_utils import train_and_evaluate
from src_training.training.training_utility.mlflow_utils import log_experiment
from src_training.mlflow.experiment_tracker import ExperimentTracker
from src_training.training.training_utility.model_registry_utils import compare_and_register_model
from configs.project_config import MODEL_NAME, EXPERIMENT_NAME, FEATURE_IMPORTANCE_PATH
from src_training.training.data.data_loader import load_data
from src_production_deployment.cloud.aws.sagemaker.tuning_enum import Algorithm, TuningStrategy
from src_training.tuning.hyperparameter_manager import HyperparameterManager
from logger.logging import setup_logging
log = setup_logging()


def main():

    X_train, y_train, X_val, Y_val = load_data()

    X_train, X_val = preprocess_data__test_target(X_train, X_val, y_train)
    
    print(X_train.dtypes, X_train.shape)
    
    print(X_val.dtypes, X_val.shape)

    #print((X_train_sample.index == y_train_sample.index).all())

    trainer = LightGBMTrainer()

    best_params = HyperparameterManager.load_best_parameters(algorithm = Algorithm.LIGHTGBM.value, stratergy = TuningStrategy.OPTUNA.value)

    tracker = ExperimentTracker(EXPERIMENT_NAME)

    with tracker.start_run(f"{Algorithm.LIGHTGBM.value}_Target_Encoding"):

        model, mae, rmse, mape, smape, wape, rmsse, training_time = train_and_evaluate(trainer, X_train, y_train, X_val, Y_val, best_params)

        importance_df = trainer.get_feature_importance(model, X_train)

        log_experiment(tracker=tracker, model=model, mae=mae, rmse=rmse, mape = mape, smape = smape, wape = wape, rmsse = rmsse , training_time=training_time, importance_df=importance_df,
                       feature_importance_path=FEATURE_IMPORTANCE_PATH, X_train_sample=X_train,alogorthm_name_tag = Algorithm.LIGHTGBM.value)
        
        print("All parameters logged to mlflow successfully")


        compare_and_register_model(tracker=tracker, rmse=rmse, rmsse = rmsse , model_name=MODEL_NAME)
    
    
if __name__ == '__main__':
    main()
    

#Path("artifacts/models").mkdir(parents=True,exist_ok=True)

#joblib.dump(model,"artifacts/models/lightgbm_baseline.pkl")

#print("Model saved successfully")



