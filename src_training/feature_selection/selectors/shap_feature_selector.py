import pandas as pd
import shap

from src_production_deployment.feature_selection.base.base_selector import BaseFeatureSelector


class SHAPFeatureSelector(BaseFeatureSelector):

    def __init__(self, model, threshold: float | None = None, top_k: int | None = None):

        self.model = model
        self.threshold = threshold
        self.top_k = top_k

        self.explainer = None
        self.shap_values = None

        self.feature_importance = None
        self.selected_features = []
        self.removed_features = []

        if top_k is not None and top_k <= 0:
         raise ValueError("top_k must be greater than 0.")

        if threshold is not None and not (0 <= threshold):
            raise ValueError("threshold must be greater than or equal to 0.")

        if top_k is None and threshold is None:
            raise ValueError("Either top_k or threshold must be provided.")
        
    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> None:

        self.explainer = shap.Explainer(self.model)

        self.shap_values = self.explainer.shap_values(X)

        importance = (abs(self.shap_values).mean(axis=0))

        self.feature_importance = (pd.DataFrame({"feature": X.columns, "importance": importance}).sort_values(by="importance", ascending=False)
            .reset_index(drop=True)
        )

        if self.top_k is not None:

            self.top_k = min(self.top_k, len(X.columns))

            self.selected_features = (self.feature_importance.head(self.top_k)["feature"].tolist())

        elif self.threshold is not None:

            self.selected_features = (self.feature_importance[self.feature_importance["importance"] > self.threshold]["feature"].tolist())

      
        self.removed_features = [feature for feature in X.columns if feature not in self.selected_features]

    def transform(self,X: pd.DataFrame) -> pd.DataFrame:

        return X[self.selected_features]

    def get_feature_importance(self) -> pd.DataFrame:
        return self.feature_importance


    def get_selected_features(self):
        return self.selected_features


    def get_removed_features(self):
        return self.removed_features


    def get_shap_values(self):
        return self.shap_values