from src_training.training.models.catboost.trainer import CatBoostTrainer
from src_training.training.training_utility.training_utils import train_and_evaluate
from src_training.training.training_utility.mlflow_utils import log_experiment
from src_training.mlflow.experiment_tracker import ExperimentTracker
from src_training.training.training_utility.model_registry_utils import compare_and_register_model
from configs.model_params import CATBOOST_HYPER_PARAMS
from configs.project_config import EXPERIMENT_NAME, FEATURE_IMPORTANCE_PATH
from logger.logging import setup_logging
log = setup_logging()
from src_training.training.data.data_loader import load_data
from src_training.encoding.encoder_processor import preprocess_data_test_target, preprocess_data_test_native
from src_production_deployment.cloud.aws.sagemaker.tuning_enum import Algorithm, TuningStrategy
from src_training.tuning.hyperparameter_manager import HyperparameterManager

def main():

    trainer = CatBoostTrainer()

    X_train, Y_train, X_val, Y_val = load_data()

    X_train, X_val  = preprocess_data_test_target(X_train, X_val,Y_train)

    print((X_train.index == Y_train.index).all())

    print(X_train.shape , Y_train.shape)

    best_params = HyperparameterManager.load_best_parameters(algorithm = Algorithm.CATBOOST.value, stratergy = TuningStrategy.OPTUNA.value)

    tracker = ExperimentTracker(EXPERIMENT_NAME)

    with tracker.start_run(f"{Algorithm.CATBOOST.value}_Target_Encoding"):

        model, mae, rmse, mape, smape, wape, rmsse, training_time = train_and_evaluate(trainer, X_train, Y_train, X_val, Y_val, best_params)

        importance_df = trainer.get_feature_importance(model, X_train)

        log_experiment(tracker=tracker, model=model, mae=mae, rmse=rmse, mape = mape, smape = smape, wape = wape, rmsse = rmsse , training_time=training_time, importance_df=importance_df,
                       feature_importance_path=FEATURE_IMPORTANCE_PATH, X_train_sample=X_train,alogorthm_name_tag =Algorithm.CATBOOST.value )
        
        print("All parameters logged to mlflow successfully")


        compare_and_register_model(tracker=tracker, rmse=rmse, rmsse = rmsse ,model_name="DemandForecasting_CatBoost_RMSSE")


if __name__ == '__main__':
    main()