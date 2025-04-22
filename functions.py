import os
import pandas as pd
import httpx
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import base64
from h2ogpte import H2OGPTE

load_dotenv()

h2ogpte_api_token = os.getenv('H2OGPTE_API_TOKEN')
openai_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


# CSV help prompt
prompt_template = PromptTemplate.from_template("""
You are a helpful assistant that converts user travel prompts into short Google search queries.

Rules:
- Extract the most relevant keywords: destination, duration, budget, group size, travel style, and interests.
- Return only a search-style keyword query. Do NOT include full sentences.
- At the end of the query, include site:.<country_code> using the official top-level domain of the destination country.

Examples:
- For Sri Lanka, use site:.lk
- For Japan, use site:.jp
- For Australia, use site:.au
- For India, use site:.in
- For the USA, skip the site: filter unless needed

Input:
{user_prompt}

Output:
""")

# Travel plan prompt
travel_prompt = PromptTemplate.from_template("""
        You are a helpful travel assistant. Use the following information to craft a personalized travel plan.

        === USER REQUEST ===
        {user_prompt}

        Respond with a daily itinerary and actionable recommendations based on the user’s interests.
        """)

travel_prompt_new = """
        You are a helpful travel assistant. Use the following information to craft a personalized travel plan.
        Respond with a daily itinerary and actionable recommendations based on the user’s interests.
        """


# Meal plan prompt
meal_prompt = PromptTemplate.from_template("""
You are a helpful travel assistant. Use the following information to craft a personalized **day-by-day meal and food experience plan**.

Please include for each day:
- 🍽️ Specific dishes for **breakfast**, **lunch**, and **dinner**
- 🏪 Restaurant, cafe, or street food suggestions (optional)
- 🌿 Regional specialties and seasonal options (if relevant)
- ✅ Tips based on dietary preferences (e.g., vegetarian, halal)
- 🎉 Bonus experiences like food markets, cooking classes, or traditional meals

Your format should be:

Day 1 – [City or Region]
- **Breakfast**: [Dish]
- **Lunch**: [Dish]
- **Dinner**: [Dish]
- *Notes: [Optional food experience or local tip]*

Repeat this format for each day of the trip.

=== USER REQUEST ===
{user_prompt}

Respond with a **clear, day-wise meal itinerary** tailored to the user's preferences and travel destination.
""")

meal_prompt_new = """
You are a helpful travel assistant. Use the following information to craft a personalized **day-by-day meal and food experience plan**.

Please include for each day:
- 🍽️ Specific dishes for **breakfast**, **lunch**, and **dinner**
- 🏪 Restaurant, cafe, or street food suggestions (optional)
- 🌿 Regional specialties and seasonal options (if relevant)
- ✅ Tips based on dietary preferences (e.g., vegetarian, halal)
- 🎉 Bonus experiences like food markets, cooking classes, or traditional meals

Your format should be:

Day 1 – [City or Region]
- **Breakfast**: [Dish]
- **Lunch**: [Dish]
- **Dinner**: [Dish]
- *Notes: [Optional food experience or local tip]*

Repeat this format for each day of the trip.

Respond with a **clear, day-wise meal itinerary** tailored to the user's preferences and travel destination.
"""



llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1,
    api_key=openai_key
)


search_query_chain = prompt_template | llm
search_query_chain_travel = travel_prompt | llm
search_query_chain_meal = travel_prompt | llm



def chatWithH2OGPTE_travel(user):
    client = H2OGPTE(
    address='https://h2ogpte.genai.h2o.ai',
    api_key=h2ogpte_api_token,
    )

    chat_session_id = client.create_chat_session()

    answer = "answer"
    
    with client.connect(chat_session_id) as session:
        reply = session.query(travel_prompt_new+f"User message: {user}")
        answer = reply.content
    return answer

def chatWithH2OGPTE_meal(user):
    client = H2OGPTE(
    address='https://h2ogpte.genai.h2o.ai',
    api_key=h2ogpte_api_token,
    )

    chat_session_id = client.create_chat_session()

    answer = "answer"
    
    with client.connect(chat_session_id) as session:
        reply = session.query(meal_prompt_new+f"User message: {user}")
        answer = reply.content
    return answer


# CSV Help function
def generate_search_query_from_prompt(prompt: str) -> str:
    """CSV Help function"""
    response = search_query_chain.invoke({"user_prompt": prompt})
    return response.content.strip()

# Travel plan generator
def generate_travel_plan(user_prompt: str) -> str:
    """Travel plan generator"""
    response = search_query_chain_travel .invoke({"user_prompt": user_prompt})
    return response.content.strip()

# Meal plan generator
def generate_meal_plan(user_prompt: str) -> str:
    """Meal plan generator"""
    response = search_query_chain_meal .invoke({"user_prompt": f"{user_prompt}, Return like markdown format"})
    return response.content.strip()



def encode_image_to_base64(path: str) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def meal(member_count, selected_country, trip_days, meal_preferences):
    return f"""
        We are a group of {member_count} people planning to visit **{selected_country}** for **{trip_days} days**.
        We are especially interested in exploring food and dining options during our stay.

        Our meal preferences are: **{", ".join(meal_preferences)}**.

        Please recommend a detailed **day-by-day meal guide** or food experience for our trip, including:
        - Must-try local dishes
        - Breakfast, lunch, and dinner suggestions (if possible)
        - Restaurants, cafes, or street food places that match our preferences
        - Any special food experiences (e.g., cooking classes, local markets)
        - Regional specialties or seasonal food options
        - Tips for eating safely and affordably in **{selected_country}**

        Tailor the plan to our **group size**, **preferences**, and the **number of days** we’ll be staying.
        """

def prompt(member_count, selected_countries, trip_days, budget, accommodation, travel_styles, meal_preferences):
    return f"""
We are a group of {member_count} people planning to visit **{selected_countries}** for **{trip_days} days**.
Our budget per person is **{budget}**. We prefer **{accommodation.lower()}** and enjoy experiences like **{", ".join(travel_styles)}**.
Our meal preferences are: **{", ".join(meal_preferences)}**.

Please create a detailed **travel itinerary** that includes:

- Popular tourist attractions  
- Cultural experiences  
- Local food & drink spots  
- Relaxing activities  
- A balance of sightseeing and free time  

Also include **travel tips and suggestions** tailored to our group size, preferences, and the time of year.
"""






# Google Search function
def google_search(query, max_results=10): 
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_api_key,
        "cx": search_engine_id,
        "q": query,
        "start": 1,
        "num": max_results
    }

    response = httpx.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])[:max_results]

    results = []
    for item in items:
        title = item.get("title", "")
        link = item.get("link", "")
        image_url = ""

        pagemap = item.get("pagemap", {})
        metatags = pagemap.get("metatags", [])

        if "cse_image" in pagemap:
            cse_images = pagemap.get("cse_image", [])
            if isinstance(cse_images, list) and cse_images:
                image_url = cse_images[0].get("src", "")
        else:
            for tag in metatags:
                if "og:image" in tag:
                    image_url = tag["og:image"]
                    break

        results.append({
            "Title": title,
            "Link": link,
            "Image": image_url
        })

    return results



# Write CSV file
def getInformationCSV(user_prompt):
    query = generate_search_query_from_prompt(user_prompt)
    results = google_search(query)
    for result in results:
        print(f"Title: {result['Title']}")
        print(f"Link: {result['Link']}")
        print(f"Image: {result['Image']}\n---")
    df = pd.DataFrame(results)
    df.to_csv("Data Source/travel_search_results.csv", index=False)
    print("✅ Results saved to 'travel_search_results.csv'")