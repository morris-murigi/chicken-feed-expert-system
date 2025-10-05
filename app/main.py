# main.py
from fastapi import FastAPI
from app.data_models import FeedQuery
from app.inference_engine import recommend_feed

app = FastAPI(title="Chicken Feed Expert System")

@app.get("/")
def root():
    return {"message": "Welcome to the Chicken Feed Expert System API"}

@app.post("/recommend")
def recommend_feed_endpoint(query: FeedQuery):
    result = recommend_feed(
        age_weeks=query.age_weeks,
        reason=query.reason,
        budget=query.budget,
        egg_production=query.egg_production,
        health=query.health,
        feed_cost_tag=query.feed_cost
    )
    return result
