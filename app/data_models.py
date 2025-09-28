from pydantic import BaseModel, Field
from typing import Optional

class FeedQuery(BaseModel):
    """
    A model representing the input query for generating chicken feed recommendations.
    
    This model defines the structure of the data required to generate tailored feed 
    recommendations based on chicken type, age, and optional conditions such as egg 
    production, feed cost, and health status.
    """
    Type: str = Field(
        ...,
        description="The type of chicken (e.g., 'Chick', 'Layer', 'Broiler Starter').",
        examples=["Chick", "Layer", "Broiler Finisher"]
    )
    Age_Weeks: float = Field(
        ...,
        description="The age of the chicken in weeks, used to determine feed requirements.",
        ge=0.0,
        examples=[2.5, 10.0, 20.0]
    )
    EggProduction: Optional[str] = Field(
        None,
        description="Optional percentage of egg production for layers (e.g., '70%').",
        examples=["70%", None]
    )
    FeedCost: Optional[str] = Field(
        None,
        description="Optional preference for feed cost (e.g., 'High', 'Low').",
        examples=["High", "Low", None]
    )
    Health: Optional[str] = Field(
        None,
        description="Optional health status of the chicken (e.g., 'Healthy', 'Sick').",
        examples=["Healthy", "Sick", None]
    )

    class Config:
        """
        Configuration for the FeedQuery model to include example data in API documentation.
        """
        schema_extra = {
            "example": {
                "Type": "Layer",
                "Age_Weeks": 20.0,
                "EggProduction": "70%",
                "FeedCost": "Low",
                "Health": "Healthy"
            }
        }
