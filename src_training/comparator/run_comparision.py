from src_training.comparator.comparison_pipeline import compare_models
from datetime import datetime

MODEL_NAMES = [
    "DemandForecasting_LightGBM_RMSSE",
    "DemandForecasting_XGBoost_RMSSE",
    "DemandForecasting_CatBoost_RMSSE"
]


def main():

    _ , champion = compare_models(MODEL_NAMES)

    print("\nChampion Model")
    print("-" * 50)
    print(f"Model          : {champion['model_name']}")
    print(f"RMSE           : {champion['rmse']:.4f}")
    print(f"MAE            : {champion['mae']:.4f}")
    print(f"RMSSE          : {champion['rmsse']:.4f}")
    print(f"Training Time  : {champion['training_time']:.2f} sec")
    print(f"Run ID         : {champion['run_id']}")

    print(f"Generated On : {datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()