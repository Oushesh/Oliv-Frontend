from google import genai
import os 
import sys
from pathlib import Path 
from dotenv import load_dotenv
from google.genai import types
from ddgs import DDGS


# Define exactly what a "Harvest Result" looks like


# Load environment variables from .env file
load_dotenv(".env")


#We can also put a test if GEMINI_API_KEY is available or not
env_path = Path(__file__).parent/".env"




###################################
"""
Chain of Thought Reasoning: 
ReACT Framework: 
Use the following question as an example: 
"""
###################################





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

def run_harvest_agent_ddgs(brand_name):
    harvest_schema = {
        "type": "OBJECT",
        "properties": {
            "brand": {"type": "STRING"},
            "harvest_found": {"type": "BOOLEAN"},
            "harvest_date": {"type": "STRING", "nullable": True},
            "confidence_score": {"type": "INTEGER", "description": "1-10 scale"},
            "source_url": {"type": "STRING"}
        },
        "required": ["brand", "harvest_found", "harvest_date"]
    }

    client = genai.Client()
    
    # 1. Get clean search data
    with DDGS() as ddgs:
        # We search specifically for the year to force recent results
        search_query = f"{brand_name} olive oil harvest official website"
        results = [f"Source: {r['href']}\nContent: {r['body']}" for r in ddgs.text(search_query, max_results=5)]
    
    web_context = "\n---\n".join(results)

    # 2. Strict System Instruction
    system_instruction = (
        "You are a precision data extraction agent. Use ONLY the provided search context. "
        "If a specific harvest year (2024, 2025, or 2026) is not explicitly mentioned, "
        "set 'harvest_found' to false. Do not use your internal knowledge of past years."
    )

    # 3. Request JSON output
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0, # No randomness
        response_mime_type="application/json",
        response_schema=harvest_schema
    )

    prompt = f"Extract harvest information for brand: {brand_name}\n\nSearch Data:\n{web_context}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config
    )
    
    return response.text



def run_harvest_agent_REACT(brand_name):
    client = genai.Client()

    # 1. Define the Structured Output Schema
    harvest_schema = {
        "type": "OBJECT",
        "properties": {
            "brand": {"type": "STRING"},
            "harvest_found": {"type": "BOOLEAN"},
            "harvest_date": {"type": "STRING", "nullable": True},
            "confidence_score": {"type": "INTEGER", "description": "1-10 scale"},
            "source_url": {"type": "STRING"}
        },
        "required": ["brand", "harvest_found", "harvest_date"]
    }

    # 2. Define the Google Search Tool
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch() 
    )

    # 3. Create the Config (Combining Search + JSON Schema)
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=harvest_schema,
        tools=[google_search_tool],
        temperature=0.0
    )

    # 4. The ReAct Instructions (System Instruction style)
    # We tell the model to use the ReAct method to fill the schema.
    instructions = f"""
    You are a research agent looking for {brand_name} olive oil harvest dates.
    
    METHOD:
    - Thought: Plan which URL to visit (start with {brand_name}.com).
    - Action: Use the 'google_search' tool to find the official site or recent press.
    - Observation: Review the search results for 2025 or 2026 dates.
    
    CRITERIA:
    - If a 2025/2026 date is found, set harvest_found to True.
    - If only older dates (2024 or earlier) exist, set harvest_found to False and harvest_date to null.
    - Return the final result in the requested JSON format.
    """

    user_prompt = f"What is the latest harvest date for {brand_name} olive oil?"

    # 5. Execute in one call
    # Gemini 3 Flash will handle the Thought/Action/Observation loop internally 
    # because the 'google_search' tool is enabled.
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[instructions, user_prompt],
        config=config
    )
    
    return response.text

# Example usage:
# print(run_harvest_agent("Cobram Estate"))



def run_harvest_agent_THOUGHT(brand_name):
    # Define exactly what a "Harvest Result" looks like
    harvest_schema = {
        "type": "OBJECT",
        "properties": {
            "brand": {"type": "STRING"},
            "harvest_found": {"type": "BOOLEAN"},
            "harvest_date": {"type": "STRING", "nullable": True},
            "confidence_score": {"type": "INTEGER", "description": "1-10 scale"},
            "source_url": {"type": "STRING"}
        },
        "required": ["brand", "harvest_found", "harvest_date"]
    }


    # Use the client initialized with your API key
    client = genai.Client()

    # 1. Define the tool using the updated 2026 'google_search' key
    # Note: 'google_search_retrieval' is for older 2.x models
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch() 
    )

    # 2. Put the tool inside a Config object
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=harvest_schema,
        tools=[google_search_tool],
        thinking_config = types.ThinkingConfig(include_thoughts=True), #<-- Enable though
        temperature=0.0 # Crucial for consistency.
    )


    prompt = (
        f"Find the harvest date for the latest batch of {brand_name} olive oil. "
        f"https:// {brand_name} .com or similar search from their similar websites."
        f"If you see a specific month/year for the year: 2025 or 2026 harvest, say 'New harvest found: [Date]'. "
        f"Otherwise, say 'NOT FOUND'."
    )

    ReACT_prompt = (
        f"""
                Task: Find the harvest date for the latest batch of {brand_name} olive oil.

                Rules:
                1. You must follow the Thought / Action / Observation loop.
                2. Use Thought to plan the search and evaluate the results found.
                3. Use Action to search Google, visit {brand_name}.com, or search similar retail sites.
                4. If you find a specific month/year for the 2025 or 2026 harvest, your final answer must be: "New harvest found: [Date]".
                5. If no 2025/2026 date is found after searching, your final answer must be: "NOT FOUND".
                """
        )


    ##ReAct Based Prompt.
    
    # 3. CRITICAL: Pass the config here!
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=ReACT_prompt,
        config=config  # <--- This activates the search 
    )
    

    # iterate through parts to find the 'thought' part or the 'text' part
    for part in response.candidates[0].content.parts:
        if part.thought:
            print (f"🧠 THOUGHT: {part.text}")
        elif part.text:
            print (f"📄 FINAL JSON: {part.text}")


    # Also extract the actual search queries used (The "Actions")
    if response.candidates[0].grounding_metadata:
        queries = response.candidates[0].grounding_metadata.web_search_queries
        if queries:
            print (f"🔍 ACTIONS (Search Queries): {queries}")
    return response.text

def test_gemini():
    from google import genai
    # The client gets the api key from the environment variable
    # 'GEMINI_API_KEY'

    #TODO: make it a try and catch block
   
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
    print (f"Test Results: {result}")

    print("Hello from olivbackend!")
    brand_name_OlvLimit = "OlvLimit"

    result = run_harvest_agent_THOUGHT(brand_name_OlvLimit)
    print (f"Gemini says : {result}")

    #brand_name_Pamako = "Pamako"
    #run_harvest_agent(brand_name_Pamako)
    
    #result = run_harvest_agent_ddgs(brand_name_OlvLimit)
    #print (f"Gemini + Duckduckgo say: {result} after manual searching")

if __name__ == "__main__":
    main()


# We can go deeper and make the agent more complicated --> Decision Making Process
# Example Filter from database, metadata and guessing or inferring date from

## Here itself for the agent we can say Enable Billing or use: duckduckgo-search
## To get the results myself


## Build this like a state machine so the agent has a fallback in case  


## Refer to documentaion of response schema: 


## Make the comparison between getsolio and OlvLimits


## How do I check ghost companies? I check their email domain? and see how it works.
## Company is active so no ghost companies.

## 


