# app/data_models.py
from pydantic import BaseModel
from typing import Optional

class RecommendRequest(BaseModel):
    type: str                 # Chicken type: Chick/Pullet/Layer/Broiler/Kienyeji
    age_weeks: int            # Age in weeks
    include_recipes: Optional[bool] = True
