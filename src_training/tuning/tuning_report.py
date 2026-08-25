from src_training.ensemble.tuning_enum import TuningStrategy


class TuningReporter:
    def __init__(self,best_params,best_score):
        self.best_params = best_params
        self.best_score = best_score
        #self.best_estimator = best_estimator

    def display(self):
        print("\n")
        print("=" * 70)
        print(f"{TuningStrategy.OPTUNA.value}_Report")
        print("=" * 70)

        print(f"Best RMSE : {self.best_score:.4f}")
        print("=" * 70)
        print("\nBest Parameters")
        print("=" * 70)
        for parameter, value in self.best_params.items():
            print(f"{parameter:<25}: {value}")
        print("=" * 70)
    
     


