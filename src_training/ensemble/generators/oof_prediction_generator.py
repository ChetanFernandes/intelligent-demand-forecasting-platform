from src_training.ensemble.generators.base_prediction_generator import BasePredictionGenerator
from src_training.ensemble.models.prediction_set import PredictionSet
from src_training.ensemble.models.ensemble_model import EnsembleModel
from sklearn.base import clone
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

class OOFPredictionGenerator(BasePredictionGenerator):
    ''' This is for stacking stratergy'''

    def __init__(self, n_splits: int = 5, shuffle: bool = True, random_state: int = 42):
                
                self.kfold = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)

    def generate(self, ensemble_model: EnsembleModel, X: pd.DataFrame, y: np.ndarray ) -> PredictionSet:

        prediction_dict  = {}

        categorical_columns = ["item_id", "dept_id", "cat_id", "store_id", "state_id", "event_name_1", "event_type_1"]

        for model_name, model in ensemble_model.models.items():

            print(f"\nTraining {model_name}")

            oof_predictions = np.zeros(len(X))

            for fold, (train_index, valid_index) in enumerate(self.kfold.split(X)):
                print(f"Fold {fold}/5")
                X_train = X.iloc[train_index] # Take only the training rows
                X_valid = X.iloc[valid_index] # Take only the validation rows.
                y_train = y.iloc[train_index] # Training targets.

                fold_model = clone(model) # clone() creates a fresh, unfitted copy.

                if isinstance(fold_model,CatBoostRegressor):

                    fold_model.fit(
                                    X_train,
                                    y_train,
                                    cat_features=categorical_columns,
                                    )
                    
                else:

                    fold_model.fit(X_train, y_train,) # Train the model using the current fold's training data.
                    
   
                predictions = fold_model.predict(X_valid) # Predict only the validation fold.
                print(f"Finished Fold {fold}")
                
                oof_predictions[valid_index] = predictions

            print("Training final model on full dataset...")

            if isinstance(model, CatBoostRegressor):

                model.fit(X,y,cat_features=categorical_columns) 
            else:
                model.fit(X, y) # Train Original Model on Full Dataset (once)

            print("Finished training final model.")

            prediction_dict[model_name] = oof_predictions
        

        return PredictionSet(predictions=prediction_dict)
