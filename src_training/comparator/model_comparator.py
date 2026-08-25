import pandas as pd

class ModelComparator:
    def __init__(self):
        self.results = []

    def add_results(self,result:dict):
        self.results.append(result)

    def compare(self):
        if not self.results:
            raise ValueError("No model results available for comparision")
        
        results_df = pd.DataFrame(self.results)

        results_df = results_df.sort_values(by = ["rmse","rmsse","training_time" , "mae" ,"mape","smape","wape",],ascending=[True,True,True,True,True,True,True]).reset_index(drop = True)

        results_df["Rank"] = results_df.index + 1

        results_df = results_df[
            [
                "Rank",
                "model_name",
                "rmse",
                "mae",
                "mape",
                "smape",
                "wape",
                "rmsse",
                "training_time",
                "run_id"
            ]
        ]

        results_df = results_df.round({
                "rmse": 4,
                "mae": 4,
                "mape":4,
                "smape":4,
                "wape":4,
                "rmsse":4,
                "training_time": 2
            })

        champion = results_df.iloc[0].to_dict()

        return results_df, champion  
