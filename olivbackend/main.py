from google import genai
import os 
import sys
from pathlib import Path 
from dotenv import load_dotenv
from google.genai import types


# Load environment variables from .env file
load_dotenv(".env")

#We can also put a test if GEMINI_API_KEY is available or not
env_path = Path(__file__).parent/".env"


def check_env():
    """Verify the API key is acutally loaded"""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key: 
        print ("x Error: GEMINI_API_KEY not found or .env file")
        print (f"Checked Path:{env_path.absolute()}")
    # Optional: Mask the key for a "success" printout
    masked_key = f"{api_key[:4]}...{api_key[-4:]}"
    print(f"✅ Environment loaded successfully. Key: {masked_key}")


## Add models from a list of models from the background

"""
Model from Background: 
gemini-2.0-flash
gemini-1.5-flash
"""

"""
Function: Take the Brand name and perform the Harvest call
2 scenarios: Olvlimit, Pamako
"""

from duckduckgo_search import DDGS

def run_harvest_agent_no_tool(brand_name):
    client = genai.Client()
    
    # 1. Manually search for free using DuckDuckGo
    with DDGS() as ddgs:
        # Get the first 3 snippets from the web
        results = [r['body'] for r in ddgs.text(f"{brand_name} olive oil harvest 2025", max_results=3)]
    
    web_context = "\n".join(results)

    # 2. Feed that text to Gemini (this uses the normal text quota, NOT the tool quota)
    prompt = f"""
    Web Search Results:
    {web_context}

    Task: Based on the search results above, find the harvest date for {brand_name}.
    If found, say 'New harvest found: [Date]'.
    If not found, say 'NOT FOUND'.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
        # config=config  <-- REMOVE the tools config here!
    )
    
    return response.text


def run_harvest_agent_manual(brand_name):
    client = genai.Client()
    
    # Get the web data for FREE (no API cost, no 20-request limit)
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(f"{brand_name} olv limits", max_results=3)]
    
    context = "\n".join(results)
    prompt = f"Using this web data:\n{context}\n\nWhat is the harvest date for {brand_name}?"

    # Call Gemini WITHOUT the search tool
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text


def run_harvest_agent(brand_name):
    # Use the client initialized with your API key
    client = genai.Client()

    # 1. Define the tool using the updated 2026 'google_search' key
    # Note: 'google_search_retrieval' is for older 2.x models
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch() 
    )

    # 2. Put the tool inside a Config object
    config = types.GenerateContentConfig(
        tools=[google_search_tool],
        temperature=1.0 # Recommended for grounding to encourage searching
    )

    prompt = (
        f"Find the harvest date for the latest batch of {brand_name} olive oil. "
        f"Search the official website for '{brand_name}' and check for any 'New Harvest' announcements. "
        f"If you see a specific month/year for the 2025 or 2026 harvest, say 'New harvest found: [Date]'. "
        f"Otherwise, say 'NOT FOUND'."
    )
    
    # 3. CRITICAL: Pass the config here!
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config  # <--- This activates the search
    )
    
    return response.text

def test_gemini():
    from google import genai
    # The client gets the api key from the environment variable
    # 'GEMINI_API_KEY'

    #TODO: make it a try and catch block
    try: 
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
        )

    # Check if response.text is acutally a string or not.
    assert isinstance(response.text,str)==True
    return (response.text)


def main():
    check_env()
    result = test_gemini()
    print (f"Gemini says: {result}")

    print("Hello from olivbackend!")
    brand_name_OlvLimit = "OlvLimit"

    result=run_harvest_agent(brand_name_OlvLimit)
    print (f"Gemini says: {result}")

    #brand_name_Pamako = "Pamako"
    #run_harvest_agent(brand_name_Pamako)
    result = run_harvest_agent_manual(brand_name_OlvLimit)
    print (f"Gemini says: {result}")


if __name__ == "__main__":
    main()


# We can go deeper and make the agent more complicated --> Decision Making Process
# Example Filter from database, metadata and guessing or inferring date from


## Here itself for the agent we can say Enable Billing or use: duckduckgo-search
## To get the results myself