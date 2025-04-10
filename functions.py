def software_search_tool(query: str) -> str:
    from dotenv import load_dotenv
    import os, httpx

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    response = google_search(api_key, search_engine_id, query)
    items = response.get("items", [])
    
    top_results = []
    for item in items[:3]:  # limit to top 3 to keep response concise
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        top_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")

    return "\n---\n".join(top_results) or "No results found."


from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)  # or any other LLM you're using

tools = [
    Tool(
        name="SoftwareSearch",
        func=software_search_tool,
        description="Use this to search for user-friendly software like video editors, IDEs, or tools based on keywords or platform."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

agent.run("Find a good free video editing software for Linux beginners.")