from pathlib import Path
import yaml
import pandas as pd
import numpy as np
from configs.project_config import HYPERPARAMETER_DIR

class HyperparameterManager:

    @staticmethod
    def save(parameters:dict, filepath: Path):

        filepath.parent.mkdir(parents=True,exist_ok=True)

        serializable_parms = {}

        for key,value in parameters.items():

            if isinstance(value, np.integer):
                serializable_parms[key] = int(value)

            elif isinstance(value,np.floating):
                serializable_parms[key] = float(value)

            else:
                serializable_parms[key] = value

        with open(filepath,"w") as file:

            yaml.safe_dump(serializable_parms, file, sort_keys = False)

    @staticmethod
    def load(filepath: Path):
        with open(filepath, "r") as file:
            return yaml.safe_load(file)
        

    @staticmethod
    def save_csv_results(results,algorithm,stratergy):
        results_df = pd.DataFrame(results)
        artifacts_dir  = Path("artifacts")
        report_path = artifacts_dir/"tuning_report"/algorithm/f"{stratergy}_results.csv"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(report_path,index=False)


    def load_best_parameters(algorithm, stratergy):
        config_path = (HYPERPARAMETER_DIR /algorithm / f"{stratergy}.yaml")
        best_params = HyperparameterManager.load(config_path)
        return best_params



