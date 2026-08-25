from ray import tune

from src_training.tuning.progress.progress_reporter import ProgressReporter


class RayProgressReporter(ProgressReporter):
    def report(self, metric, step):
        print(f"Reporting Fold {step} RMSE={metric}")
        tune.report(
            {
                "rmse": metric,
                "step": step
            }
        )