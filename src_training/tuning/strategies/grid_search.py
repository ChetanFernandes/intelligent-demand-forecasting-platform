from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
from src_training.tuning.strategies.base_stratergy import BaseTuningStrategy
import pandas as pd

class GridsearchTuner(BaseTuningStrategy):
    def __init__(self,estimator,parameter_space, scoring = "neg_root_mean_squared_error", n_splits = 2, n_jobs = -1):
        self.estimator = estimator
        self.parameter_space = parameter_space
        self.scoring = scoring
        self.n_splits = n_splits # n_splits means training is divided in two splits. Split 1 - Train and Validation. Split 2 - Train and Validation
        self.n_jobs = n_jobs

        


    def fit(self,x_train,y_train):


        time_series_split  = TimeSeriesSplit(n_splits = self.n_splits)

        self.grid_search = GridSearchCV(estimator=self.estimator, param_grid=self.parameter_space, scoring=self.scoring,cv=time_series_split, n_jobs=self.n_jobs, verbose=2, refit=False)
        
        self.grid_search.fit(x_train,y_train)

        # We dont use early stopping for grid search as internally it splits data into train and val

    def get_best_params(self):
        return self.grid_search.best_params_
    
    def get_best_score(self):
        return abs(self.grid_search.best_score_)
    
    def get_best_estimator(self):
        return self.grid_search.best_estimator_
    
    def get_cv_results(self):
        results = pd.DataFrame(self.grid_search.cv_results_)
        results = results.sort_values("rank_test_score")
        return results
    
'''
Total Model Fits
=
(Number of parameter combinations) *  (Number of CV splits)

'''