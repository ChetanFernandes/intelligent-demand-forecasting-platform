from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class Wrapper(ABC):
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass