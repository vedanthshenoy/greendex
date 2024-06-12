import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from typing import Dict

# Load environment variables from the .env file
load_dotenv()

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.5)

# Define a prompt template
prompt_template = """
You are an experienced environmental analyst. A user wants to understand the environmental problems in {area} between {start_year} and {end_year}, the promises made by political parties to address these issues, and information about forest coverage, water coverage, and greener coverage during that period. Here are the raw search results:

{search_results}

Please analyze these search results and use the information to provide a comprehensive overview, focusing on the specified year range ({start_year} to {end_year}). Be sure to cite specific information from the search results when appropriate. Your response should be in the following format:

1. Major Environmental Problems in {area} ({start_year} to {end_year})
   - Problem 1
   - Problem 2
   - Problem 3
   - (Add more as necessary)

2. Political Parties' Promises and Plans in that {area} ({start_year} to {end_year})
   - Party 1:
     - Promise 1 (including promises related to forest coverage, water coverage, and greener coverage)
     - Promise 2
     - (Add more as necessary)
   - Party 2:
     - Promise 1 (including promises related to forest coverage, water coverage, and greener coverage)
     - Promise 2
     - (Add more as necessary)

3. Forest Coverage in {area} ({start_year} to {end_year})
   - (Provide details on forest coverage during the specified year range)

4. Water Coverage in {area} ({start_year} to {end_year})
   - (Provide details on water coverage during the specified year range)

5. Greener Coverage in {area} ({start_year} to {end_year})
   - (Provide details on greener coverage during the specified year range)

6. Key Insights from Search Results ({start_year} to {end_year}):
   - Insight 1
   - Insight 2
   - (Add more as necessary)

Your Response:
"""

prompt = PromptTemplate(
    input_variables=["area", "start_year", "end_year", "search_results"],
    template=prompt_template
)

# Create a function to perform the web search and structure the data
def search(search_query: str) -> str:
    """Search the web for information on a given topic"""
    search_tool = DuckDuckGoSearchRun()
    search_results = search_tool.run(search_query)
    return search_results

def process_input(inputs: Dict[str, str]) -> Dict[str, str]:
    """
    Process the input data and perform a web search.

    Args:
        inputs: A dictionary containing the area, start year, and end year.

    Returns:
        A dictionary containing the area, start year, end year, and search results.
    """
    area = inputs["area"]
    start_year = inputs["start_year"]
    end_year = inputs["end_year"]
    search_query = f"environmental problems, political parties promises, forest coverage, water coverage, greener coverage in {area} from {start_year} to {end_year}"
    search_results = search(search_query)
    return {"area": area, "start_year": start_year, "end_year": end_year, "search_results": search_results}

# Set up the RunnableSequence
chain = (
    RunnablePassthrough() |
    process_input |
    prompt |
    llm
)

# Main function to handle user input and generate the response
def get_environmental_info(area: str, start_year: str, end_year: str) -> str:
    """
    Get environmental information for a given area and year range.

    Args:
        area: The area to search for (eg: california).
        start_year: The start year of the range (eg: 2020).
        end_year: The end year of the range (eg: 2023).

    Returns:
        A string containing the generated environmental information report.
    """
    response = chain.invoke({"area": area, "start_year": start_year, "end_year": end_year})
    return response.content

# Example usage
area = input("Enter the area (eg: california): ")
start_year = input("Enter the start year (eg: 2020): ")
end_year = input("Enter the end year (eg: 2023): ")
response = get_environmental_info(area, start_year, end_year)
print(response)