from fastapi import FastAPI
from app.data_models import FeedQuery
from app.inference_engine import apply_rules, get_feed_recipe

app = FastAPI(title="Chicken Feed Expert System")

@app.get("/")
def root():
    return {"message": "Welcome to the Chicken Feed Expert System API"}

@app.post("/recommend")
def recommend_feed(query: FeedQuery):
    facts = query.dict()
    recommendations = apply_rules(facts)

    # Attach feed formulation if available
    feed_type = None
    for rec in recommendations:
        if "Recommend" in rec:
            feed_type = rec["Recommend"]
            break

    recipe = get_feed_recipe(feed_type) if feed_type else {}
    return {"facts": facts, "recommendations": recommendations, "recipe": recipe}
