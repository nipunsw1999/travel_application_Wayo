# app.py

import streamlit as st
import pycountry


st.set_page_config(page_title="🌍 Travel Assistant", layout="centered")

st.title("✈️ Travel Recommendation Assistant")
st.markdown("Ask travel questions like destinations, budget trips, or visa-free countries!")

query = st.text_input("Where do you want to go? 🌴")

country_list = sorted([country.name for country in pycountry.countries])
selected_countries = st.selectbox(
    "Select countries you want to visit:",
    options=country_list,
)
member_count = st.number_input("How many people are traveling?", min_value=1, max_value=10, value=2)


trip_days = st.number_input("How many days is your trip?", min_value=1, max_value=30, value=7)


prompt = f"""
We are a group of {member_count} people planning to visit {selected_countries} for {trip_days} days. 
Please create a detailed travel itinerary that includes popular tourist attractions, cultural experiences, food recommendations, and some relaxing activities.

Make sure the plan balances sightseeing and free time. Also include travel tips and suggestions tailored to the number of people and duration.
"""

st.write(prompt)