from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import TimeSeriesSplit
from src_training.tuning.strategies.base_stratergy import BaseTuningStrategy
import pandas as pd
from catboost import CatBoostRegressor

class RandomsearchTuner(BaseTuningStrategy):
    def __init__(self,estimator, parameter_space, n_iter=20, random_state = 42, scoring="neg_root_mean_squared_error", n_splits = 4, n_jobs= 1):
        self.estimator = estimator
        self.parameter_space = parameter_space
        self.scoring = scoring
        self.n_splits = n_splits
        self.n_jobs = n_jobs
        self.n_iter = n_iter
        self.random_state = random_state


    def fit(self,x_train,y_train):

        time_series_split  = TimeSeriesSplit(n_splits = self.n_splits)

        self.random_search = RandomizedSearchCV(estimator=self.estimator,param_distributions=self.parameter_space ,n_iter=self.n_iter,scoring=self.scoring,cv=time_series_split,random_state=self.random_state,
                                                n_jobs=self.n_jobs, verbose=2,refit=False)

        if isinstance(self.estimator, CatBoostRegressor):

            category_columns = x_train.select_dtypes(include="category").columns.tolist()

            self.random_search.fit(
                x_train,
                y_train,
                cat_features=category_columns
            )
        else:

            self.random_search.fit(x_train,y_train)

        # GridSearchCV and RandomizedSearchCV perform internal cross-validation. so it dont support early stopping
        
    
    def get_best_params(self):
        return self.random_search.best_params_
    
    def get_best_score(self):
        return abs(self.random_search.best_score_)
    
    def get_best_estimator(self):
        return self.random_search.best_estimator_
    
    def get_cv_results(self):
        results = pd.DataFrame(self.random_search.cv_results_)
        results = results.sort_values("rank_test_score")
        return results

'''
Total model fits
=
n_iter *  Number of CV splits
'''