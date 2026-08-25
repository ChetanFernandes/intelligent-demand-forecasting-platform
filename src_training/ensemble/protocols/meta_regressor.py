from typing import Protocol
import numpy as np

class MetaRegressor(Protocol):
    ''' Anything that as fit and predict can be used as metamodel'''
    def fit(self,X:np.ndarray, y:np.ndarray) -> None:
        pass
    def predict(self,X: np.ndarray) -> np.ndarray:
        ...
