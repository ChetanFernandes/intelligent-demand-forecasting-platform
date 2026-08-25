import pandas as pd
from src_training.feature_selection.factory.feature_selection_factory import FeatureSelectedFactory

class FeatureSelectionPipeline:

    def __init__(self,selector_name:str,**selector_params):
        
        self.selector = FeatureSelectedFactory.create(selector_name,**selector_params)

    def run(self,X_train:pd.DataFrame, X_test:pd.DataFrame,y_train:pd.Series| None = None) -> tuple[pd.DataFrame,pd.DataFrame]:

        X_train_selected = self.selector.fit_transform(X_train, y_train)

        X_test_selected = self.selector.transform(X_test)

        metadata = {
        "selected_features": self.selector.get_selected_features(),
        "removed_features": self.selector.get_removed_features(),
    }

        return X_train_selected, X_test_selected, metadata
        

