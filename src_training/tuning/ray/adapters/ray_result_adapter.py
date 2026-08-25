import pandas as pd

class RayResultAdapter:

    def __init__(self, result_grid, metric):
        self.result_grid = result_grid
        self.metric = metric
        self.best_result = result_grid.get_best_result()

    def get_best_params(self):
        return self.best_result.config

    def get_best_score(self):
        return self.best_result.metrics[self.metric]

    def get_cv_results(self):

        rows = []

        valid_results = [r for r in self.result_grid if self.metric in r.metrics]

        sorted_results = sorted(valid_results, key = lambda r : r.metrics[self.metric])
           
        rows = []

        for rank, result in enumerate(sorted_results, start=1):
            row = {
                    "Rank": rank,
                    self.metric: result.metrics[self.metric],
                    **result.config,
                  }

            rows.append(row)

        return pd.DataFrame(rows)