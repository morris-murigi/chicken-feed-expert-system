import streamlit as st
import requests

st.title("🐔 Chicken Feed Expert System")

age = st.number_input("Enter Age (weeks):", min_value=0.0, step=0.5)
reason = st.selectbox("Reason for rearing:", ["Eggs", "Meat"])
budget = st.radio("Budget:", ["optimum", "low"])
egg_prod = st.text_input("Egg Production % (optional):", "")
health = st.selectbox("Health Status:", ["Healthy", "Sick", ""])
feed_cost_tag = st.selectbox("Feed Cost Tag:", ["Normal", "High", ""])

if st.button("Get Recommendation"):
    payload = {
        "age_weeks": age,
        "reason": reason,
        "budget": budget,
        "egg_production": egg_prod if egg_prod else None,
        "health": health if health else None,
        "feed_cost": feed_cost_tag if feed_cost_tag else None
    }
    res = requests.post("http://localhost:8000/recommend", json=payload)

    if res.status_code == 200:
        data = res.json()
        st.json(data)  # debug raw output

        st.subheader("Detected Chicken Type")
        st.write(f"Frame: {data['detected_frame']}")
        st.write(f"Age Label: {data['detected_age_label']} (degree={data['detected_degree']})")

        st.subheader("Recommendations")
        for rec in data["recommendations"]:
            st.write(f"- {rec.get('Recommend','')} | Advice: {rec.get('Advice','')}")

        if data["recipe_name"]:
            st.subheader(f"Feed Recipe: {data['recipe_name']}")
            st.write("Ingredients Breakdown:")
            for ing, details in data["cost_breakdown"]["ingredients"].items():
                st.write(f"{ing}: {details['qty_kg']} kg x {details['price_per_kg']} = {details['cost']}")
            st.write(f"**Total Cost:** {data['cost_breakdown']['total_cost']}")
            st.write(f"**Cost per kg:** {data['cost_breakdown']['cost_per_kg']}")
    else:
        st.error("Error fetching recommendations from backend.")
