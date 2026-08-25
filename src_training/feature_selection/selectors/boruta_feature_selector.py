import pandas as pd
#pip install Boruta
from boruta import BorutaPy

from src_production_deployment.feature_selection.base.base_feature_selector import BaseFeatureSelector


class BorutaFeatureSelector(BaseFeatureSelector):

    def __init__(
        self,
        model,
        n_estimators="auto",
        perc=100,
        alpha=0.05,
        max_iter=100,
        random_state=42,

    ):

        self.model = model
        self.n_estimators = n_estimators
        self.perc = perc
        self.alpha = alpha
        self.max_iter = max_iter
        self.random_state = random_state

        self.selector = None

        self.selected_features = []
        self.removed_features = []
        self.feature_ranking = None
        if max_iter <= 0:
            raise ValueError("max_iter must be greater than 0.")

        if alpha <= 0 or alpha >= 1:
            raise ValueError("alpha must be between 0 and 1.")

        if perc <= 0 or perc > 100:
            raise ValueError("perc must be between 1 and 100.")

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> None:

        self.selector = BorutaPy(
            estimator=self.model,
            n_estimators=self.n_estimators,
            perc=self.perc,
            alpha=self.alpha,
            max_iter=self.max_iter,
            random_state=self.random_state,
            verbose=0,
        )

        self.selector.fit(
            X.values,
            y.values,
        )

        self.selected_features = (
            X.columns[self.selector.support_]
            .tolist()
        )

        self.removed_features = (
            X.columns[~self.selector.support_]
            .tolist()
        )

        self.feature_ranking = (
            pd.DataFrame({
                "feature": X.columns,
                "ranking": self.selector.ranking_,
            })
            .sort_values("ranking")
            .reset_index(drop=True)
        )

    def transform(
        self,
        X: pd.DataFrame,
    ) -> pd.DataFrame:

        return X[self.selected_features]

    def get_selected_features(self):

        return self.selected_features

    def get_removed_features(self):

        return self.removed_features

    def get_feature_ranking(self):

        return self.feature_ranking

'''
    Boruta requires the estimator to expose a feature_importances_ attribute after fitting. It works well with:

✅ DecisionTreeRegressor / DecisionTreeClassifier
✅ RandomForestRegressor / RandomForestClassifier
✅ ExtraTreesRegressor / ExtraTreesClassifier

It is not intended for models like:

❌ Linear Regression
❌ Logistic Regression
❌ SVM
❌ KNN

Although some users adapt Boruta for boosting models, the library is primarily designed around Random Forest–style estimators. For your framework, it's best to document Boruta as an optional selector for tree ensembles rather than a universally applicable feature selection method.
'''