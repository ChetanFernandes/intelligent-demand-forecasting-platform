from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EnsembleModel:
    """
    Holds trained base models.
    """
    models: dict[str, Any]

 