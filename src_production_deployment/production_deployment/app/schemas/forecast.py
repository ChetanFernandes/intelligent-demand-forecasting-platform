from pydantic import BaseModel, Field
from typing import Any

class ForecastRequest(BaseModel):
    forecast_days: int = Field(gt=0,le=28) #greater than(gt)
   


class PredictionItem(BaseModel):
    id: str
    day: str
    sales: float


class ForecastResponse(BaseModel):
    request_id: str
    forecast_days : int
    model_version: str
    predictions: list [dict[str,Any]]


