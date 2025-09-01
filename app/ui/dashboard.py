import streamlit as st
import requests

API_URL = "http://localhost:8000/recommend"  # Update when deploying

st.title("🐓 Chicken Feed Expert System")
st.write("Get feed recommendations based on chicken type, age, and conditions.")

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
