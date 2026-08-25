import optuna
from src_training.tuning.progress.progress_reporter import ProgressReporter

class OptunaProgressReporter(ProgressReporter):

    def __init__(self, trial):

        self.trial = trial

    def report(self, metric, step):

        self.trial.report(metric, step)

        if self.trial.should_prune():

            raise optuna.TrialPruned(
                f"Trial pruned at step {step}"
            )