from pydantic import BaseModel
from typing import Optional

class FeedQuery(BaseModel):
    Type: str
    Age_Weeks: float
    EggProduction: Optional[str] = None
    FeedCost: Optional[str] = None
    Health: Optional[str] = None