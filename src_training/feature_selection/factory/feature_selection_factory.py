from src_training.feature_selection.base.base_selector import BaseFeatureSelector
from src_training.feature_selection.selectors.correlation_feature_selector import CorrelationFeatureSelector
from src_training.feature_selection.selectors.permutation_feature_selector import PermutationFeatureSelector
from src_production_deployment.feature_selection.selectors.shap_feature_selector import SHAPFeatureSelector
from src_production_deployment.feature_selection.selectors.rfe_feature_selector import RFEFeatureSelector

class FeatureSelectedFactory:
    @staticmethod
    def create(selector_name:str, **kwargs) -> BaseFeatureSelector:

        selector_name = selector_name.lower()

        selectors = {"correlation": CorrelationFeatureSelector,
                     "permutation": PermutationFeatureSelector,
                      "shap": SHAPFeatureSelector,
                       "rfe": RFEFeatureSelector,
                        # "boruta": BorutaFeatureSelector,
                    }

        if selector_name not in selectors:
            raise ValueError(
                f"Unsupported feature selector: {selector_name}"
            )

        return selectors[selector_name](**kwargs)