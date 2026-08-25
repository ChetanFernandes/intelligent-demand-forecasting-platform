from src_training.tuning.strategies.optuna.algorithms_engines.catboost.cat_boost_training import CatBoostTrainingEngine
from src_training.tuning.parameter_space.parameter_space_converter import ParameterSpaceConverter
from src_training.tuning.progress.optuna_progress_reporter import OptunaProgressReporter

class CatBoostObjective:
    ''' Ask engine to train -> Select optimization metric -> Return it to Optuna'''

    def __init__(self,estimator, parameter_space, X_train, y_train, n_splits = 4):

        self.estimator = estimator
        self.parameter_space = parameter_space
        self.X_train = X_train
        self.y_train = y_train
        self.n_splits = n_splits

    def __call__(self, trial): # Python allows objects with __call__ to behave like functions. By Python converts it to obj.__call__(). 
        # Therefore Optuna can simply do

        params = ParameterSpaceConverter.to_optuna(self.parameter_space,trial)
       
        engine = CatBoostTrainingEngine(estimator=self.estimator, X_train=self.X_train, y_train=self.y_train, n_splits=self.n_splits)

        progress_reporter = OptunaProgressReporter(trial)

        metrics = engine.evaluate(params=params, progress_reporter = progress_reporter)

        return metrics["rmse"] 