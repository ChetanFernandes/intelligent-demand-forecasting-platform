from src_training.ensemble.wrappers.wrapper import Wrapper
from src_training.ensemble.models.ensemble_model import EnsembleModel
import numpy as np
import pandas as pd

class BlendedWrapper(Wrapper):
    def __init__(self, ensemble_model : EnsembleModel, meta_model):
        self.ensemble_model = ensemble_model
        self.meta_model = meta_model

    def predict(self, X:pd.DataFrame) -> np.ndarray :

        predictions = []
        
        for model in self.ensemble_model.models.values():
            predictions.append(model.predict(X))

        predictions = np.column_stack(predictions)

        return self.meta_model.predict(predictions)

            
