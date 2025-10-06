import streamlit as st
import requests

st.title("🐔 Chicken Feed Expert System")

# --- Input fields ---
age = st.number_input("Enter Age (weeks):", min_value=0.0, step=0.5)
reason = st.selectbox("Reason for rearing:", ["Eggs", "Meat"])
budget = st.radio("Budget:", ["optimum", "low"])
egg_prod = st.text_input("Egg Production % (optional):", "")
health = st.selectbox("Health Status:", ["Healthy", "Sick", ""])
feed_cost_tag = st.selectbox("Feed Cost Tag:", ["Normal", "High", ""])

# --- Submit button ---
if st.button("Get Recommendation"):
    payload = {
        "type": reason,                                # matches FeedQuery.type
        "age_weeks": age,
        "egg_production": egg_prod if egg_prod else None,
        "feed_cost": feed_cost_tag if feed_cost_tag else None,
        "health": health if health else None,
        "budget": budget                               # ✅ now included
    }

    try:
        res = requests.post("http://localhost:8000/recommend", json=payload)

        if res.status_code == 200:
            data = res.json()
            st.json(data)  # debug raw output (you can remove later)

            # --- Display results ---
            st.subheader("Detected Chicken Type")
            st.write(f"Frame: {data.get('detected_frame', 'N/A')}")
            st.write(f"Age Label: {data.get('detected_age_label', 'N/A')} (degree={data.get('detected_degree', 'N/A')})")

            st.subheader("Recommendations")
            for rec in data.get("recommendations", []):
                st.write(f"- {rec.get('Recommend','')} | Advice: {rec.get('Advice','')}")

            # --- Optional recipe section ---
            if data.get("recipe_name"):
                st.subheader(f"Feed Recipe: {data['recipe_name']}")
                st.write("Ingredients Breakdown:")

                cost_breakdown = data.get("cost_breakdown", {})
                ingredients = cost_breakdown.get("ingredients", {})
                for ing, details in ingredients.items():
                    st.write(f"{ing}: {details['qty_kg']} kg x {details['price_per_kg']} = {details['cost']}")

                st.write(f"**Total Cost:** {cost_breakdown.get('total_cost', 'N/A')}")
                st.write(f"**Cost per kg:** {cost_breakdown.get('cost_per_kg', 'N/A')}")
        else:
            st.error(f"Error fetching recommendations from backend. Status code: {res.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to backend. Make sure FastAPI is running at http://localhost:8000")
