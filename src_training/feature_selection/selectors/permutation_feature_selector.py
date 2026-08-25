import pandas as pd
from sklearn.inspection import permutation_importance
from src_training.feature_selection.base.base_selector import BaseFeatureSelector

class PermutationFeatureSelector(BaseFeatureSelector):
    def __init__(self,model,threshold:float = 0.0 , scoring : str = "neg_root_mean_squared_error", n_repeats: int = 10, random_state:int = 10):
        self.model = model
        self.threshold = threshold
        self.scoring = scoring
        self.n_repeats = n_repeats
        self.random_state = random_state
        self.importance_scores = None
        self.selected_features = []
        self.removed_features = []

    
    def fit(self,x:pd.DataFrame,y:pd.Series | None = None) ->None:
        result= permutation_importance(estimator=self.model, X = x, y = y, scoring=self.scoring, n_repeats=self.n_repeats, random_state=self.random_state)


        self.importance_scores = (pd.DataFrame ({"feature" : x.columns, "importance" : result.importances_mean})).sort_values(by = "importance", ascending = False).reset_index(drop = True)

        self.selected_features = self.importance_scores[self.importance_scores > self.threshold].index.tolist()

        self.removed_features = [ feature for feature in x.columns if feature not in self.selected_features]

    def transform(self, x:pd.DataFrame) -> pd.DataFrame:
        return x[self.selected_features]


    def get_feature_importance(self) -> pd.DataFrame:
        return self.importance_scores


    def get_selected_features(self):
        return self.selected_features


    def get_removed_features(self):
        return self.removed_features
