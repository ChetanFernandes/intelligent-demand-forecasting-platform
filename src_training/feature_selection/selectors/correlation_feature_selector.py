import pandas as pd
import numpy as np
from src_training.feature_selection.base.base_selector import BaseFeatureSelector

class CorrelationFeatureSelector(BaseFeatureSelector):
    """
    Removes highly correlated features.

    """

    def __init__(self, threshold : float = 0.90):

        if not 0 < threshold < 1:
             raise ValueError("threshold must be between 0 and 1.")

        self.threshold = threshold
        self.selected_features = []
        self.removed_features = []
        self.correlation_matrix = None

    def fit(self,X:pd.DataFrame,Y:pd.Series | None = None) ->None:

        if X.empty:
            raise ValueError("Input DF is empty")

        if X.shape[1] < 2:
            raise ValueError( "Correlation filtering requires at least two features.")

        self.correlation_matrix = X.corr().abs()

        upper_triangle = self.correlation_matrix.where(np.triu(np.ones(self.correlation_matrix.shape), k=1).astype(bool))

        self.removed_features = [ column for column in upper_triangle.columns if any(upper_triangle[column] > self.threshold)]

        self.selected_features = [ column for column in X.columns if column not in self.removed_features]

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        if not self.selected_features:
            raise RuntimeError("Feature selector has not been fitted.")
        return X[self.selected_features]

    def get_selected_features(self) -> list[str]:
        """
        Returns the selected feature names.
        """
        return self.selected_features


    def get_removed_features(self) -> list[str]:
        """
        Returns the removed feature names.
        """
        return self.removed_features


    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Returns the computed correlation matrix.
        """
        return self.correlation_matrix


