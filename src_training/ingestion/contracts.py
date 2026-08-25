from dataclasses import dataclass
import pandas as pd

@dataclass
class ForecastDataset:
    sales: pd.DataFrame | None  = None #Type hint
    calendar: pd.DataFrame | None  = None
    prices: pd.DataFrame | None  = None
