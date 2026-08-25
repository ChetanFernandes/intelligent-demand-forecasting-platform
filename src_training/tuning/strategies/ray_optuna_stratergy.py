from ray import tune
from ray.tune import Tuner
from ray.tune.search.optuna import OptunaSearch
from src_training.tuning.ray.adapters.ray_result_adapter import RayResultAdapter
import pandas as pd
from src_training.tuning.ray.trainables.light_gbm_ray_trainables import light_gbm_trainable
from src_training.tuning.parameter_space.parameter_space_converter import ParameterSpaceConverter
from ray.tune.schedulers import ASHAScheduler
'''
Its responsibility is orchestration:

Build the search algorithm (OptunaSearch)
Create the search space
Inject dependencies using tune.with_parameters()
Configure the Tuner
Execute tuner.fit()
Return the results

This is exactly where tune.with_parameters() belongs.
'''

class RayOptunaStrategy():

    def __init__(self,estimator,parameter_space,algorithm, n_trials=20, scoring= "rmse",n_splits=4,random_state=42, mode = "min"):

        self.estimator = estimator
        self.parameter_space = parameter_space
        self.algorithm = algorithm
        self.n_trials = n_trials
        self.scoring = scoring
        self.n_splits = n_splits
        self.random_state = random_state
        self.mode = mode

    def scheduler(self):
        return ASHAScheduler(
                            max_t= self.n_splits,
                            grace_period=2,
                            reduction_factor=2,
                            time_attr="step",
                           )
    
    def fit(self, X_train, y_train):
        
        # Wrap the trainable with additional dependencies
        wrapped_trainable = tune.with_parameters(light_gbm_trainable, estimator =  self.estimator , X_train=X_train , y_train=y_train, 
                                                 n_splits = self.n_splits)
        
        ray_space = ParameterSpaceConverter.to_ray( self.parameter_space)


        optuna_search = OptunaSearch()

        def short_trial_dirname(trial):
            return f"trial_{trial.trial_id}"

        # create tuner
        tuner = Tuner(
                    trainable = wrapped_trainable,
                    param_space =  ray_space,
                    tune_config=tune.TuneConfig(
                        metric= self.scoring ,
                        mode= self.mode,
                        search_alg = optuna_search,
                        num_samples=self.n_trials ,
                        trial_dirname_creator=short_trial_dirname,
                        scheduler = self.scheduler(),
                    ),
                )

        # Executing stratergy

        result_grid = tuner.fit()

        self.result_adapter = RayResultAdapter(result_grid=result_grid, metric =  self.scoring)
    
    def get_best_params(self) -> dict:
        return self.result_adapter.get_best_params()

    def get_best_score(self) -> float:
        return self.result_adapter.get_best_score()

    def get_cv_results(self) -> pd.DataFrame:
        return self.result_adapter.get_cv_results()


























        