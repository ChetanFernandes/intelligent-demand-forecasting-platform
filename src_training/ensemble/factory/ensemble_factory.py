from src_training.ensemble.strategies.simple_average_strategy import SimpleAverageStrategy
from src_training.ensemble.strategies.weighted_average_strategy import WeightAverageStrategy
from src_training.ensemble.strategies.blending_stratergy import BlendingStratergy
from src_training.ensemble.strategies.stacking import StackingStrategy
from src_training.ensemble.config.ensemble_config import EnsembleConfig

class EnsembleFactory:

    @staticmethod
    def create(config: EnsembleConfig):
        
        if config.stratergy == "simple_average":
            return SimpleAverageStrategy()

        if config.stratergy == "weighted_average":
            return WeightAverageStrategy(
                weights = config.weights
            )

        if config.stratergy == "blending":
            return BlendingStratergy(
                meta_model = config.meta_model
            )
        if config.stratergy == "stacking":
            return StackingStrategy(
                meta_model = config.meta_model
            )
        
        raise ValueError(
            f"Unknown strategy '{config.strategy}'"
        )