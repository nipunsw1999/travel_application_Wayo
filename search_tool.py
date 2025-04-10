# search_tool.py

import os
from dotenv import load_dotenv
import httpx
from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI

load_dotenv()

def google_search(api_key, search_engine_id, query, **params):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, **params}
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()

def software_search_tool(query: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    response = google_search(api_key, search_engine_id, query)
    items = response.get("items", [])
    
    top_results = []
    for item in items[:3]:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        top_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")

    return "\n---\n".join(top_results) or "No results found."

def get_agent():
    tool = Tool(
        name="SoftwareSearch",
        func=software_search_tool,
        description="Use this to search for user-friendly software based on keywords or platform."
    )
    llm = ChatOpenAI(temperature=0)
    return initialize_agent([tool], llm, agent="zero-shot-react-description", verbose=True)
