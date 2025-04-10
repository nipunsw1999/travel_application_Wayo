# app.py

import streamlit as st
import pycountry
from functions import generate_search_query_from_prompt,getInformationCSV,generate_travel_plan

st.set_page_config(page_title="🌍 Travel Assistant", layout="centered")

st.title("✈️ Travel Recommendation Assistant")
st.markdown("Ask travel questions like destinations, budget trips, or visa-free countries!")

country_list = sorted([country.name for country in pycountry.countries])
selected_countries = st.selectbox(
    "Select countries you want to visit:",
    options=country_list,
)
member_count = st.number_input("How many people are traveling?", min_value=1, max_value=10, value=2)


trip_days = st.number_input("How many days is your trip?", min_value=1, max_value=30, value=7)

travel_styles = st.multiselect(
    "What kind of experiences are you looking for?",
    ["Nature", "Adventure", "Beach", "Culture & History", "Luxury", "Budget", "Food & Drink", "Nightlife", "Wellness & Spa", "Shopping"],
    default=["Culture & History", "Food & Drink"]
)

budget = st.selectbox(
    "What’s your budget range per person?",
    ["<$500", "$500 - $1000", "$1000 - $2000", "$2000+"],
    index=1
)

accommodation = st.radio(
    "Preferred accommodation type:",
    ["Hotels", "Hostels", "Resorts", "Airbnb", "Camping"]
)


prompt = f"""
We are a group of {member_count} people planning to visit {selected_countries} for {trip_days} days.
Our budget per person is {budget}. We prefer {accommodation.lower()} and enjoy experiences like {", ".join(travel_styles)}.

Please create a detailed travel itinerary that includes:
- Popular tourist attractions
- Cultural experiences
- Local food & drink spots
- Relaxing activities
- A balance of sightseeing and free time

Also include travel tips and suggestions tailored to our group size, preferences, and the time of year.
"""

start = st.button("Start")

if start:
    with st.spinner("Generating..."):
        sub_prompt = generate_search_query_from_prompt(prompt)
        st.write()
        getInformationCSV(sub_prompt)
        plan = generate_travel_plan(prompt)
        st.write(prompt)
        st.write(plan)