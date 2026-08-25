import json
from pathlib import Path
import pandas as pd

class FeatureSelectionManager:
    @staticmethod
    def save_selected_features(features:list[str], output_dir:str) ->None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with open(Path(output_dir)/ "selected_features.json", "w") as file:
            json.dump(features, file, indent = 4)


    @staticmethod
    def save_removed_features(features:list[str], output_dir:str) -> None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with open(Path(output_dir) / "removed_features.json", "w") as file:
            json.dump(features, file, indent= 5)


    @staticmethod
    def save_feature_importance(importance: pd.DataFrame, output_dir: str) -> None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        importance.to_csv(Path(output_dir) / "feature_importance.csv", index=False)

    @staticmethod
    def save_correlation_matrix(correlation_matrix: pd.DataFrame, output_dir: str ) -> None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        correlation_matrix.to_csv(Path(output_dir) / "correlation_matrix.csv")

    