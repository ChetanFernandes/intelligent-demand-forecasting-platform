from abc import ABC, abstractmethod
from typing import Any
from src_training.ensemble.models.prediction_set import PredictionSet
import pandas as pd

class BasePredictionGenerator(ABC):

    @abstractmethod
    def generate(self, models: dict[str, Any], X: pd.DataFrame) -> PredictionSet:
        pass