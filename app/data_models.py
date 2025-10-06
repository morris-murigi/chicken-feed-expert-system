# data_models.py
from pydantic import BaseModel
from typing import Optional

class FeedQuery(BaseModel):
    """
    Defines the structure of the request body for the /recommend endpoint.
    """
    type: str                       # Reason for rearing (Eggs or Meat)
    age_weeks: float                # Age of the chicken in weeks
    egg_production: Optional[str] = None  # Optional egg production percentage
    feed_cost: Optional[str] = None       # Feed cost tag (e.g., Normal, High)
    health: Optional[str] = None          # Health status (Healthy, Sick)
    budget: Optional[str] = None          # Budget type (optimum, low)