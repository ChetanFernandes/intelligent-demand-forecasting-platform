import pandas as pd
from sklearn.feature_selection import RFECV
from src_production_deployment.feature_selection.base.base_feature_selector import BaseFeatureSelector


class RFEFeatureSelector(BaseFeatureSelector):

    def __init__(self, model, n_features_to_select: int, step: int = 1,):

        self.model = model
        self.n_features_to_select = n_features_to_select
        self.step = step

        self.selector = None

        self.selected_features = []
        self.removed_features = []
        self.feature_ranking = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:

        self.selector = RFECV(estimator=self.model, n_features_to_select=self.n_features_to_select, step=self.step)

        self.selector.fit(X, y)

        self.selected_features = (X.columns[self.selector.support_].tolist())

        self.removed_features = (X.columns[~self.selector.support_].tolist())

        self.feature_ranking = (pd.DataFrame({
                "feature": X.columns,
                "ranking": self.selector.ranking_
            })
            .sort_values("ranking")
            .reset_index(drop=True)
        )

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        return X[self.selected_features]

    def get_selected_features(self):
        return self.selected_features


    def get_removed_features(self):
        return self.removed_features


    def get_feature_ranking(self):
        return self.feature_ranking