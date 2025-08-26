# dashboard.py
import streamlit as st
import requests
import threading
import uvicorn
from fastapi import FastAPI
from app.data_models import FeedQuery
from app.inference_engine import apply_rules, get_feed_recipe

# -------------------------------
# Define backend (FastAPI)
# -------------------------------
backend = FastAPI(title="Chicken Feed Expert System")

@backend.get("/")
def root():
    return {"message": "Welcome to the Chicken Feed Expert System API"}

@backend.post("/recommend")
def recommend_feed(query: FeedQuery):
    facts = query.dict()
    recommendations = apply_rules(facts)
    feed_type = None
    for rec in recommendations:
        if "Recommend" in rec:
            feed_type = rec["Recommend"]
            break
    recipe = get_feed_recipe(feed_type) if feed_type else {}
    return {"facts": facts, "recommendations": recommendations, "recipe": recipe}

# Run backend in a background thread
def run_backend():
    uvicorn.run(backend, host="0.0.0.0", port=8000)

threading.Thread(target=run_backend, daemon=True).start()

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🐓 Chicken Feed Expert System")
st.write("Get feed recommendations based on chicken type, age, and conditions.")

API_URL = "http://localhost:8000/recommend"

with st.form("feed_form"):
    chicken_type = st.selectbox("Chicken Type", ["Chick", "Pullets / Growers", "Layer", 
                                                 "Broiler Starter", "Broiler Grower", "Broiler Finisher"])
    age_weeks = st.number_input("Age (weeks)", min_value=0.0, step=0.5)
    egg_production = st.text_input("Egg Production (%) (optional)")
    feed_cost = st.selectbox("Feed Cost (optional)", ["", "High", "Low"])
    health = st.selectbox("Health (optional)", ["", "Healthy", "Sick"])
    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    payload = {
        "Type": chicken_type,
        "Age_Weeks": age_weeks,
        "EggProduction": egg_production if egg_production else None,
        "FeedCost": feed_cost if feed_cost else None,
        "Health": health if health else None
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.subheader("Recommendations")
            for rec in data["recommendations"]:
                st.json(rec)
            if data["recipe"]:
                st.subheader("Suggested Recipe")
                st.write(data["recipe"]["Ingredients"])
        else:
            st.error("Error fetching recommendations.")
    except Exception as e:
        st.error(f"Backend not available: {e}")
