import streamlit as st
import requests
import threading
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from app.data_models import FeedQuery
from app.inference_engine import apply_rules, get_feed_recipe

# -------------------------------
# Define backend (FastAPI)
# -------------------------------
backend = FastAPI(
    title="Chicken Feed Expert System",
    description="A professional API for generating optimized chicken feed recommendations based on poultry needs.",
    version="1.0.0",
    docs_url="/docs",
    openapi_tags=[
        {
            "name": "Feed Recommendations",
            "description": "Endpoints for generating chicken feed recommendations and recipes."
        }
    ]
)

# Define response models for clarity
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

@backend.get(
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

@backend.post(
    "/recommend",
    response_model=FeedRecommendationResponse,
    summary="Generate Feed Recommendation",
    description="Receives poultry data and returns tailored feed recommendations and a detailed recipe.",
    tags=["Feed Recommendations"]
)
def recommend_feed(query: FeedQuery):
    facts = query.dict()
    recommendations = apply_rules(facts)
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

# Run backend in a background thread
def run_backend():
    uvicorn.run(backend, host="0.0.0.0", port=8000)

threading.Thread(target=run_backend, daemon=True).start()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Chicken Feed Expert System", page_icon="??", layout="wide")

# Sidebar for navigation and branding
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=Logo", caption="Chicken Feed Expert System")
    st.markdown("### About")
    st.markdown("Optimize poultry nutrition with tailored feed recommendations based on chicken type, age, and conditions.")
    st.markdown("---")
    st.markdown("© 2025 Chicken Feed Expert System")

# Main content
st.title("?? Chicken Feed Expert System")
st.markdown("**Get tailored feed recommendations to optimize your poultry's health and productivity.**")

API_URL = "http://localhost:8000/recommend"

# Form styling with better organization
with st.form("feed_form", clear_on_submit=False):
    st.markdown("### Input Poultry Details")
    col1, col2 = st.columns(2)
    with col1:
        chicken_type = st.selectbox(
            "Chicken Type", 
            ["Chick", "Pullets / Growers", "Layer", "Broiler Starter", "Broiler Grower", "Broiler Finisher"],
            help="Select the type of chicken"
        )
        age_weeks = st.number_input(
            "Age (weeks)", 
            min_value=0.0, 
            step=0.5, 
            format="%.1f", 
            help="Enter the age of the chicken in weeks"
        )
    with col2:
        egg_production = st.text_input(
            "Egg Production (%) (optional)", 
            help="Enter egg production percentage, if applicable"
        )
        feed_cost = st.selectbox(
            "Feed Cost (optional)", 
            ["", "High", "Low"], 
            help="Select feed cost preference, if any"
        )
        health = st.selectbox(
            "Health (optional)", 
            ["", "Healthy", "Sick"], 
            help="Select the health status of the chicken, if known"
        )
    submitted = st.form_submit_button("Get Recommendation", use_container_width=True)

# Handle form submission
if submitted:
    payload = {
        "Type": chicken_type,
        "Age_Weeks": age_weeks,
        "EggProduction": egg_production if egg_production else None,
        "FeedCost": feed_cost if feed_cost else None,
        "Health": health if health else None
    }
    try:
        with st.spinner("Fetching recommendations..."):
            response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success("Recommendation generated successfully!")
            
            # Display facts
            st.subheader("Input Facts")
            st.json(data["facts"], expanded=False)
            
            # Display recommendations
            st.subheader("Recommendations")
            if data["recommendations"]:
                for rec in data["recommendations"]:
                    st.markdown(f"- {rec}")
            else:
                st.info("No recommendations matched.")
            
            # Display recipe
            st.subheader("Suggested Recipe")
            if data["recipe"]:
                st.markdown(f"**Recipe Name:** {data['recipe'].get('name', 'N/A')}")
                st.markdown(f"**Target DCP:** {data['recipe'].get('target_dcp', 'N/A')}")
                if data["recipe"].get("ingredients"):
                    st.markdown("**Ingredients:**")
                    for ingredient, qty in data["recipe"]["ingredients"].items():
                        st.markdown(f"- {ingredient}: {qty} kg")
            else:
                st.info("No recipe available for this chicken type.")
        else:
            st.error(f"Error fetching recommendations: HTTP {response.status_code}")
    except Exception as e:
        st.error(f"Backend not available: {str(e)}")
