from src_training.ensemble.strategies.blending_stratergy import BlendingStratergy
from src_training.ensemble.protocols.meta_regressor import MetaRegressor


class StackingStrategy(BlendingStratergy):
    def __init__(self, meta_model: MetaRegressor):

        super().__init__(meta_model)

    @property
    def name(self):
        return "Stacking"