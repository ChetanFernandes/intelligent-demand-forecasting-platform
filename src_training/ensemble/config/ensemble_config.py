from dataclasses import dataclass
from src_training.ensemble.protocols.meta_regressor import MetaRegressor

@dataclass(frozen = True, slots = True)
class EnsembleConfig:
    stratergy:str
    weights: dict[str,float] | None = None
    meta_model:MetaRegressor | None = None

    def to_mlflow_params(self) -> dict:
        
        params = {"ensemble_type" : self.stratergy}

        if self.weights is not None:
            params.update(self.weights)

        if self.meta_model is not None:
            params["meta_model"] = self.meta_model.__class__.__name__

        return params