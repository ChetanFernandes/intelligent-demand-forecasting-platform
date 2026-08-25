from abc import ABC, abstractmethod
import pandas as pd

class BaseFeatureSelector:
    '''
        Abstract base class for all feature selection techniques.
    '''
    @abstractmethod
    def fit(self, x:pd.DataFrame, y:pd.Series | None = None) -> None:
        """
        learn which feature to be selected
        """

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Return dataframe containing selected features.
        """
        pass

    def fit_transform(self, X: pd.DataFrame, y: pd.Series | None = None) -> pd.DataFrame:
        """
        Fit selector and transform dataset.
        """
        self.fit(X, y)
        
        return self.transform(X)