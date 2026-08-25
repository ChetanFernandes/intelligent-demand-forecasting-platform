from src_training.ensemble.base.base_ensemble import BaseEnsemble
from src_training.ensemble.models.prediction_set import PredictionSet
import numpy as np

class WeightAverageStrategy(BaseEnsemble):

    def __init__(self,weights:dict[str,float]):
    
        if not weights:
            raise ValueError("Weights cannot be empty.")

        
        for value in weights.values():
            if value < 0:
                raise ValueError("Weights are negative")

        total_weight = sum(weights.values())


        if total_weight <= 0:
            raise ValueError("Sum of weights must be greater than zero.")

        self.weights = {
            model: weight / total_weight
            for model, weight in weights.items()
        }

    @property
    def name(self):
        return "weighted_average"

    def aggregate(self, prediction_set : PredictionSet) -> np.ndarray:

        prediction_models = set(prediction_set.get_model_name())

        weighted_models = set(self.weights.keys())

        missing = prediction_models - weighted_models

        if missing:
            raise ValueError(f"Missing weigts for models: {missing}")

        extra = weighted_models - prediction_models

        if extra:
            raise ValueError(f"Unused weights supplied: {missing}")

        weighted_predictions = []
        
        for model_name, prediction in prediction_set.predictions.items():

            weights = self.weights[model_name]

            weighted_predictions.append(prediction * weights)

        return np.sum(weighted_predictions, axis=0)




