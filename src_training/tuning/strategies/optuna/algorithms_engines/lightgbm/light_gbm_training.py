import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error
from lightgbm import early_stopping

class LightGBMTrainingEngine:
    ''' Train -> Evaluate -> Return all metrics'''

    def __init__(self, estimator, X_train, y_train, n_splits=4):

        self.estimator = estimator
        self.X_train = X_train
        self.y_train = y_train
        self.n_splits = n_splits

    def evaluate(self, params,  progress_reporter = None):

        time_series_split = TimeSeriesSplit(n_splits=self.n_splits)

        scores = []

        for fold, (train_index, validation_index) in enumerate(time_series_split.split(self.X_train), start=1):

            X_train_fold = self.X_train.iloc[train_index]
            X_validation_fold = self.X_train.iloc[validation_index]

            y_train_fold = self.y_train.iloc[train_index]
            y_validation_fold = self.y_train.iloc[validation_index]

            model = self.estimator.__class__(random_state = 42, **params) 

            '''
            # "Give me the class of this estimator."
            # model = LGBMRegressor(
                    random_state=42,
                    learning_rate=0.05,
                    num_leaves=31,
                    max_depth=6,
                    n_estimators=150
                )
            '''

            #model.fit(X_train_fold, y_train_fold)
            
            model.fit(X_train_fold,y_train_fold, eval_set = [(X_validation_fold,y_validation_fold)], eval_metric = "rmse",
                      callbacks = [early_stopping(stopping_rounds=50, verbose = True)])

            # Here if you notice I am using model level (LightGBM) early stopping. I have not used it for Gird and Random becuase it not straight forward

            predictions = model.predict(X_validation_fold)

            rmse = root_mean_squared_error(y_validation_fold, predictions)

            scores.append(rmse)

            if progress_reporter is not None:
                    progress_reporter.report(metric=np.mean(scores), step=fold)

        average_rmse = np.mean(scores)

        return {
                    "rmse": average_rmse,
                    "fold_scores": scores
                }