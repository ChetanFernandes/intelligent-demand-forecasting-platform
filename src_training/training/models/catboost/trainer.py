from catboost import CatBoostRegressor
import pandas as pd

class CatBoostTrainer:
      
    def train(self, X_train, y_train, X_val, Y_val, **model_params):
        """ use this when youre experiemnting"""
        
        model = CatBoostRegressor(random_state = 42, loss_function="RMSE", eval_metric="RMSE", early_stopping_rounds=50,
                                  use_best_model=True, **model_params)

        '''
        categorical_features = [
                                    "item_id",
                                    "dept_id",
                                    "cat_id",
                                    "store_id",
                                    "state_id",
                                    "event_name_1",
                                    "event_type_1"
                                ]
        '''

        model.fit(X_train, y_train, eval_set= [(X_val,Y_val)],verbose = True)
   

        return model
    
    

    def get_feature_importance(self, model, X_train):

        importance_df = pd.DataFrame({"feature": X_train.columns, "importance": model.feature_importances_})
        importance_df = importance_df.sort_values(by="importance", ascending=False)
        return importance_df