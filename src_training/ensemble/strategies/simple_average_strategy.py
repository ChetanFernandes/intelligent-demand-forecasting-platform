import numpy as np
from src_training.ensemble.base.base_ensemble import BaseEnsemble
from src_training.ensemble.models.prediction_set import PredictionSet


class SimpleAverageStrategy(BaseEnsemble):
    @property
    def name(self):
        return "simple_average"

    def aggregate(self, prediction_set: PredictionSet) -> np.ndarray:
        matrix = prediction_set.get_matrix()
        return matrix.mean(axis=1)

