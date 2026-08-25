from src_training.ensemble.base.base_learning_ensemble import BaselearningEnsemble
from src_training.ensemble.models.prediction_set import PredictionSet
import numpy as np
from src_training.ensemble.protocols.meta_regressor import MetaRegressor

class BlendingStratergy(BaselearningEnsemble):
    def __init__(self, meta_model : MetaRegressor):
        self.meta_model = meta_model

    def fit(self,prediction_set: PredictionSet, y_true : np.ndarray) -> None:
        ''' Use metal model to train on prediction made by base models'''
        X = prediction_set.get_matrix()
        self.meta_model.fit(X, y_true)

    def predict(self, prediction_set:PredictionSet) -> np.ndarray:
        X = prediction_set.get_matrix()
        return self.meta_model.predict(X)

    @property
    def name(self):
        return "Blending"

    @property
    def model(self):
        return self.meta_model 
