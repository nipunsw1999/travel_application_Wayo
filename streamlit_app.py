import streamlit as st
import pycountry
from functions import chatWithH2OGPTE_travel,prompt,chatWithH2OGPTE_meal,generate_search_query_from_prompt,getInformationCSV,generate_travel_plan,generate_meal_plan
import pandas as pd

st.set_page_config(page_title="🌍 Wayo Assistant", layout="centered")

st.title("✈️ Wayo Travel Recommendation")
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
meal_preferences = st.multiselect(
    "Do you have any meal preferences?",
    ["Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher", "Seafood", "Local Cuisine", "No Preference"],
    default=["Local Cuisine"]
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
Our budget per person is {budget}. We prefer {accommodation.lower()} and enjoy experiences like {", ".join(travel_styles)}. Our meal preferences {meal_preferences}

Please create a detailed travel itinerary that includes:
- Popular tourist attractions
- Cultural experiences
- Local food & drink spots
- Relaxing activities
- A balance of sightseeing and free time

Also include travel tips and suggestions tailored to our group size, preferences, and the time of year.
"""

meal_prompt = f"""
We are a group of {member_count} people planning to visit {selected_countries} for {trip_days} days.
We are especially interested in exploring food and dining options during our stay.

Our meal preferences are: {", ".join(meal_preferences)}.

Please recommend a day-by-day meal guide or food experience for the trip, including:
- Must-try local dishes
- Breakfast, lunch, and dinner suggestions (if possible)
- Restaurants, cafes, or street food places that match our preferences
- Any special food experiences (e.g., cooking classes, local markets)
- Regional specialties or seasonal food options
- Tips for eating safely and affordably in {selected_countries}

Tailor the plan to our group size, preferences, and the number of days we’ll be staying.
"""


start = st.button("Start")

if start:
    with st.spinner("Generating..."):
        sub_prompt = generate_search_query_from_prompt(prompt)
        getInformationCSV(sub_prompt)
        
        plan = generate_travel_plan(prompt)
    
        st.title("Plan")
        st.write(plan)
        
        meal_plan = generate_meal_plan(meal_prompt)
        
        st.title("Meal plan")
        st.write(meal_plan)
        
        # CSV file google search api
        df = pd.read_csv("Data Source/travel_search_results.csv")
        image_column = df.columns[-1]
        for index, row in df.iterrows():
            title = row["Title"]
            link = row["Link"]
            image_url = row[image_column]

            st.markdown(f"### [{title}]({link})")

            if (
                pd.notna(image_url) and
                image_url.startswith(('http://', 'https://', '//')) and
                not image_url.startswith("x-raw-image://")
            ):
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                st.image(image_url, width=500)


            st.markdown("---")