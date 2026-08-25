from pathlib import Path

LOOKBACK_DAYS = 365
MODEL_NAME = "DemandForecasting_LightGBM_RMSSE"
EXPERIMENT_NAME = "Demand Forecasting"
TRAIN_SAMPLE_SIZE = 500000
RANDOM_STATE = 54
FEATURE_IMPORTANCE_PATH = "artifacts/feature_importance.csv"

CONFIG_DIR = Path("configs")
HYPERPARAMETER_DIR = CONFIG_DIR / "hyperparameters"
AWSBUCKET = "faang-ml-platform"
EXECUTION_ROLE = 'arn:aws:iam::135053048192:role/SageMakerExecutionRole'
PROCESSED_DATASET_DIR = "artifacts/datasets/data_split"

AZURE_ACCOUNT_NAME = "stdemandforecastingdev"
AZURE_FILESYSTEM = "demand-forecasting"
