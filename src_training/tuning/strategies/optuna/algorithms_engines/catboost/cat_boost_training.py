import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error


class CatBoostTrainingEngine:
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
            # time_series_split.split() returns indices, not the actual data.

            X_train_fold = self.X_train.iloc[train_index] # Extract the data
            X_validation_fold = self.X_train.iloc[validation_index] # Extract the data

            y_train_fold = self.y_train.iloc[train_index]
            y_validation_fold = self.y_train.iloc[validation_index]

            model = self.estimator.__class__(random_state = 42, loss_function="RMSE", eval_metric="RMSE", early_stopping_rounds=50,
                                             use_best_model=True, **params) 

            #model.fit(X_train_fold, y_train_fold)

            #categorical_columns = ["item_id", "dept_id", "cat_id", "store_id", "state_id", "event_name_1", "event_type_1"]
            #print(X_train_fold[categorical_columns].dtypes)
            
            model.fit(X_train_fold,y_train_fold, eval_set = (X_validation_fold,y_validation_fold), verbose = True,
                )

            '''
            Why don't you use the original validation set during Optuna tuning?

             A strong answer is: "The original validation set is kept completely separate to provide an unbiased evaluation 
             after hyperparameter tuning. During tuning, I perform TimeSeriesSplit only on the training data. 
             Each fold has its own validation portion for early stopping and scoring. 
             This prevents the hyperparameter search from repeatedly seeing the held-out validation set and overfitting to it."
            '''


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