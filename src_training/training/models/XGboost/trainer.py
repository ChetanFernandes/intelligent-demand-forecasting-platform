from xgboost import XGBRegressor
import pandas as pd

class XGBoostTrainer:
      
    def train(self, X_train, y_train, X_val, Y_val,**model_params):
        """ use this when youre experiemnting"""
        
        model = XGBRegressor(random_state = 42, eval_metric="rmse", early_stopping_rounds=50, enable_categorical=False, **model_params)

        model.fit(X_train, y_train, eval_set=[(X_val, Y_val)],verbose = True)

        return model
    
    

    def get_feature_importance(self, model, X_train):

        importance_df = pd.DataFrame({"feature": X_train.columns, "importance": model.feature_importances_})

        importance_df = importance_df.sort_values(by="importance", ascending=False)


        return importance_df