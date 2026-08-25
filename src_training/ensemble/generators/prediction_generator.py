from src_training.ensemble.generators.base_prediction_generator import BasePredictionGenerator
from src_training.ensemble.models.prediction_set import PredictionSet
from src_training.ensemble.models.ensemble_model import EnsembleModel
import pandas as pd


class PredictionGenerator(BasePredictionGenerator):
    """ This is for bledninf=g"""

    def generate(self, ensemble_model: EnsembleModel, X:pd.DataFrame) -> PredictionSet:

        predictions = {}

        for model_name, model in ensemble_model.models.items():

            predictions[model_name] = model.predict(X)

        return PredictionSet(predictions=predictions)