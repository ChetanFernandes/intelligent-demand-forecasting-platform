from abc import ABC, abstractmethod
from src_training.ensemble.models.prediction_set import PredictionSet
from src_training.ensemble.models.ensemble_result import EnsembleResult

class BaseEnsemble(ABC):
    """
    Base class for all ensemble strategies.
    
    """
 
    @abstractmethod
    def aggregate(self, prediction_set: PredictionSet) -> EnsembleResult:
        """
        Generate ensemble predictions.
        """
        pass