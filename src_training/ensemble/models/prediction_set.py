from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True, slots=True)
class PredictionSet:
    """
    Holds predictions from multiple base models.

    Example:
        {
            "xgboost": np.ndarray,
            "lightgbm": np.ndarray,
            "catboost": np.ndarray
        }
    """
    predictions: dict[str, np.ndarray]

    def __post__init__(self):
        # Because with a dataclass, Python creates the __init__() for you.
        #  After initialization, it automatically calls __post_init__(), making it the right place for validatio
        lengths = {len(pred) for pred in self.predictions.values() }

        if len(lengths) != 1:
            raise ValueError(
                "All prediction arrays must have the same length."
            )
               
    def get_matrix(self) -> np.ndarray:
        return np.column_stack(list(self.predictions.values()))

    def get_model_name(self) -> list[str]:
        return list(self.predictions.keys())

    def get_prediction(self, model_name: str) -> np.ndarray:
        return self.predictions[model_name]

'''
class PredictionSet:
    def __init__(self,predictions:dict[str,np.ndarray]):
        self.predictions = predictions
'''



'''
1. @dataclass

A dataclass automatically generates common methods for you.

Without a dataclass, you would write:

class PredictionSet:

    def __init__(self, predictions):
        self.predictions = predictions

    def __repr__(self):
        return f"PredictionSet(predictions={self.predictions})"

With a dataclass:

@dataclass
class PredictionSet:
    predictions: dict[str, np.ndarray]

Python automatically creates:

__init__()
__repr__()
__eq__()

for you.





'''