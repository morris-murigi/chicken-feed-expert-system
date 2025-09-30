import streamlit as st
import requests
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.inference_engine import fuzzy_recommend_broiler  # import fuzzy function

API_URL = "http://localhost:8000/recommend"  # Update when deploying

st.title("🐓 Chicken Feed Expert System")
st.write("Get feed recommendations based on chicken type, age, and conditions.")

# Mode selector
mode = st.radio("Select Reasoning Mode:", ["Crisp (Rule-Based)", "Fuzzy Logic"])

# User input form
with st.form("feed_form"):
    chicken_type = st.selectbox("Chicken Type", ["Chick", "Pullets / Growers", "Layer", 
                                                 "Broiler Starter", "Broiler Grower", "Broiler Finisher"])
    age_weeks = st.number_input("Age (weeks)", min_value=0.0, step=0.5)
    egg_production = st.text_input("Egg Production (%) (optional)")
    feed_cost = st.selectbox("Feed Cost (optional)", ["", "High", "Low"])
    health = st.selectbox("Health (optional)", ["", "Healthy", "Sick"])

    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    if mode == "Crisp (Rule-Based)":
        # Call API (existing behavior)
        payload = {
            "Type": chicken_type,
            "Age_Weeks": age_weeks,
            "EggProduction": egg_production if egg_production else None,
            "FeedCost": feed_cost if feed_cost else None,
            "Health": health if health else None
        }
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

    else:
        # Fuzzy Mode – handled locally, no API call
        st.subheader("🔮 Fuzzy Logic Recommendation")
        
        if "Broiler" in chicken_type:
            result = fuzzy_recommend_broiler(age_weeks)
            
            st.write("**Age Membership:**", result["age_membership"])
            st.write("**Protein Membership:**", result["protein_membership"])
            st.write("**Suitability Scores:**")
            for feed, score in result["options"]:
                st.write(f"- {feed}: {score}")
            
            st.success(f"Recommended Feed → {result['recommended'][0]} (Score: {result['recommended'][1]})")
        
        else:
            st.warning("Fuzzy logic currently implemented for Broilers only. Use Crisp mode for other chicken types.")
