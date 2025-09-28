from fastapi import FastAPI
from pydantic import BaseModel
from app.data_models import FeedQuery
from app.inference_engine import apply_rules, get_feed_recipe

# Initialize FastAPI with enhanced metadata for professional appearance
app = FastAPI(
    title="Chicken Feed Expert System",
    description="A professional API for recommending optimized chicken feed formulations based on poultry needs.",
    version="1.0.0",
    docs_url="/docs",
    openapi_tags=[
        {
            "name": "Feed Recommendations",
            "description": "Endpoints for generating chicken feed recommendations and recipes."
        }
    ]
)

# Define response model for clarity in API documentation
class WelcomeResponse(BaseModel):
    message: str
    version: str
    documentation: str

class FeedRecommendationResponse(BaseModel):
    facts: dict
    recommendations: list
    recipe: dict
    status: str
    message: str

@app.get(
    "/",
    response_model=WelcomeResponse,
    summary="API Welcome Endpoint",
    description="Returns a welcome message with API details for the Chicken Feed Expert System.",
    tags=["Feed Recommendations"]
)
def root():
    return {
        "message": "Welcome to the Chicken Feed Expert System API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.post(
    "/recommend",
    response_model=FeedRecommendationResponse,
    summary="Generate Feed Recommendation",
    description="Receives poultry data and returns tailored feed recommendations and a detailed recipe.",
    tags=["Feed Recommendations"]
)
def recommend_feed(query: FeedQuery):
    facts = query.dict()
    recommendations = apply_rules(facts)

    # Extract feed type from recommendations
    feed_type = None
    for rec in recommendations:
        if "Recommend" in rec:
            feed_type = rec["Recommend"]
            break

    recipe = get_feed_recipe(feed_type) if feed_type else {}
    return {
        "facts": facts,
        "recommendations": recommendations,
        "recipe": recipe,
        "status": "success",
        "message": "Feed recommendation generated successfully"
    }
