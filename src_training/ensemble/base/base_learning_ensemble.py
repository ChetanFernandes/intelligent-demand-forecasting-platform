from abc import ABC, abstractmethod
import numpy as np
from src_training.ensemble.models.prediction_set import PredictionSet

class BaselearningEnsemble(ABC):

    @abstractmethod
    def fit(self, prediction_set:PredictionSet, y_true : np.ndarray) -> None:
        """ Trains the meta model """
        pass

    @abstractmethod
    def predict(self, prediction_set: PredictionSet) -> np.ndarray:
        ''' predicts using the trained meta model'''
        pass