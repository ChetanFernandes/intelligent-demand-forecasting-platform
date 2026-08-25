from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True, slots=True)
class EnsembleResult:
    """
    Result returned by an ensemble strategy.
    """
    predictions: np.ndarray
    strategy: str
    models: list[str]

    