import streamlit as st
import requests
import asyncio
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.mcp_client import MCPClient  # Import your MCP client

API_URL = "http://localhost:8000/recommend"

st.set_page_config(page_title="Chicken Feed Expert System", page_icon="🐓")

st.title("🐓 Chicken Feed Expert System")


# Tabs
tab1, tab2 = st.tabs(["Structured Input", "Natural Language"])


# ------------------------------
# Tab 1: Structured Input
# ------------------------------
with tab1:
    st.write("Fill out structured inputs for recommendations:")

    with st.form("feed_form"):
        chicken_type = st.selectbox(
            "Chicken Type",
            ["Chick", "Pullets / Growers", "Layer",
             "Broiler Starter", "Broiler Grower", "Broiler Finisher"]
        )
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
            "Health": health if health else None,
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


# ------------------------------
# Tab 2: Natural Language Input
# ------------------------------
with tab2:
    st.write("Ask in plain language (e.g., 'What should I feed 3-week-old chicks?').")

    user_query = st.text_area("Your Question", height=100)
    if st.button("Ask"):
        if user_query.strip():
            async def run_query():
                client = MCPClient()
                await client.connect_to_server("app/mcp_server.py")  # Path to your MCP server
                #result = await client.process_query(user_query)
                result = await client.process_query(user_query, verbose=True)
                await client.cleanup()
                return result

            response = asyncio.run(run_query())
            st.subheader("Answer")
            st.write(response)
        else:
            st.warning("Please enter a question.")
