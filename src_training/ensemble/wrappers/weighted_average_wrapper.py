from src_training.ensemble.wrappers.wrapper import Wrapper
from src_training.ensemble.models.ensemble_model import EnsembleModel
import numpy as np
import pandas as pd


class WeightedAverageWrapper(Wrapper):

    def __init__(self, ensemble_model: EnsembleModel, weights: dict[str, float]):

        self.ensemble_model = ensemble_model

        self.weights = weights

    def predict(self, X: pd.DataFrame) -> np.ndarray:

        predictions = []

        for model in self.ensemble_model.models.values():

            predictions.append(model.predict(X))

        predictions = np.column_stack(predictions)

        weight_vector = np.array(list(self.weights.values()))

        return predictions @ weight_vector