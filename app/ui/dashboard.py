import streamlit as st
import requests
import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from app.data_models import FeedQuery
    st.write("Data models imported successfully.")
except ImportError as e:
    st.error(f"Import error for data_models: {str(e)}")
    st.stop()

try:
    from app.inference_engine import apply_rules, get_feed_recipe
    st.write("Inference engine imported successfully.")
except ImportError as e:
    st.error(f"Import error for inference_engine: {str(e)}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="Chicken Feed Expert System", page_icon="🐓", layout="wide")

with st.sidebar:
    st.image("https://via.placeholder.com/150?text=Logo", caption="Chicken Feed Expert System")
    st.markdown("### About")
    st.markdown("Optimize poultry nutrition with tailored feed recommendations based on chicken type, age, and conditions.")
    st.markdown("---")
    st.markdown("© 2025 Chicken Feed Expert System")

st.title("🐓 Chicken Feed Expert System")
st.markdown("**Get tailored feed recommendations to optimize your poultry's health and productivity.**")

API_URL = "http://localhost:8000/recommend"

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
        egg_production = st.slider(
            "Egg Production (%) (optional)", 
            min_value=0, 
            max_value=100, 
            value=0, 
            step=1, 
            help="Approximate egg production percentage; slide to estimate"
        )
        if egg_production == 0:
            egg_production = None
        else:
            egg_production = f"{egg_production}%"
        feed_cost = st.selectbox(
            "Feed Cost (optional)", 
            ["", "High", "Low"], 
            help="Select cost preference, if any"
        )
        health = st.selectbox(
            "Health (optional)", 
            ["", "Healthy", "Sick"], 
            help="Select health status, if known"
        )
    submitted = st.form_submit_button("Get Recommendation", use_container_width=True)

if submitted:
    payload = {
        "Type": chicken_type,
        "Age_Weeks": age_weeks,
        "EggProduction": egg_production,
        "FeedCost": feed_cost if feed_cost else None,
        "Health": health if health else None
    }
    try:
        with st.spinner("Fetching recommendations..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
        data = response.json()
        st.success("Recommendation generated successfully!")
        st.subheader("Input Facts")
        st.json(data["facts"], expanded=False)
        st.subheader("Recommendations")
        if data["recommendations"]:
            for rec in data["recommendations"]:
                st.markdown(f"- {rec}")
        else:
            st.info("No recommendations matched.")
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
    except Exception as e:
        st.error(f"Error fetching recommendations: {str(e)}")
