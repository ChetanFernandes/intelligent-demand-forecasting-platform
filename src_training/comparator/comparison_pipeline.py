from src_training.comparator.model_comparator import ModelComparator
from src_training.registry.mlflow_registry import ModelRegistry
from src_training.comparator.comparison_report import ComparisonReport


registry = ModelRegistry()

def compare_models(model_names):

    comparator = ModelComparator()

    for model_name in model_names:

        model_details = registry.get_model_details(model_name)

        print(model_details)

        if model_details is None:
            continue

        metrics = model_details["metrics"]

        comparator.add_results({
            "model_name": model_name,
            "rmse":metrics["rmse"],
            "mae":metrics["mae"],
            "mape":metrics["mape"],
            "smape":metrics["smape"],
            "wape":metrics["wape"],
            "rmsse": metrics["rmsse"],
            "training_time":metrics["training_time"],
            "run_id": model_details["run_id"]
        })

    comparision_df, champion = comparator.compare()

    ComparisonReport.generate(comparision_df,champion)

    return  comparision_df, champion


