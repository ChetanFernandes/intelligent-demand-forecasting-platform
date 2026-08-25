from lightgbm import LGBMRegressor
import pandas as pd
from lightgbm import early_stopping

class LightGBMTrainer:
      
    '''
    def train(self, X_train, y_train, **model_params):
        """ use this when youre experiemnting"""
        
        default_params = {
            "objective": "regression",
            "n_estimators": 100,
            "learning_rate": 0.1,
            "random_state": 42,
            "n_jobs": -1
        }

        default_params.update(model_params)

        model = LGBMRegressor(**default_params)

        model.fit(X_train, y_train)

        return model
    '''
    

    def train(self,X_train,y_train, X_val, Y_val, **model_params):
        ''' Use this after hypertuning'''

        model = LGBMRegressor(**model_params)
        # The ** operator unpacks a dictionary into keyword arguments.

        model.fit(X_train, y_train, eval_set= [(X_val,Y_val)], eval_metric = "rmse",
                      callbacks = [early_stopping(stopping_rounds=50, verbose = True)])

        return model
    
    
    def get_feature_importance(self, model, X_train):

        importance_df = pd.DataFrame({"feature": X_train.columns, "importance": model.feature_importances_})
        importance_df = importance_df.sort_values(by="importance", ascending=False)
        return importance_df






