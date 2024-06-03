import json
import os
from typing import List
from bs4 import BeautifulSoup
import requests
from gnews import GNews
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()


def scrape_content(url: str) -> str:
    """
    Function to scrape content from a given URL.

    Args:
        url (str): The URL to scrape content from.

    Returns:
        str: The scraped content.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.text for p in paragraphs])
    return content

def get_news(location: str, period: str) -> None:
    """
    Function to get environmental news for a given location and period.

    Args:
        location (str): The location for which news needs to be fetched.
        period (str): The period for which news needs to be fetched.
                      It can be h (hours), d (days), m (months), or y (years).
                      Example: '1y' for 1 year.
    """
    google_news = GNews(max_results=5, period=period)
    news_items = google_news.get_news(f'{location}: environmental')

    all_contents = ""
    for item in news_items:
        url = item['url']
        content = scrape_content(url)
        all_contents += content + "\n"

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        google_api_key = input("Provide your Google API Key: ")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    Prompt_temp = PromptTemplate.from_template
    (
    "You are an Expert New writer and your task is to take the provided text_context and convert it into comprehensive summary"
    "The summary should capture the main points and key details of the text while conveying the author's intended meaning accurately."
    "Please ensure that the summary is well-organized and easy to read, with clear headings and subheadings to guide the reader through each section."
    "The length of the summary should be appropriate to capture the main points and key details of the text, without including unnecessary information or becoming overly long."
    "The text_context: {text_context}"
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=Prompt_temp,
        verbose=True
    )
    
    text_context = all_contents
    result = chain.invoke(input=text_context)
    summary = result

    # Extracting "text" from the result
    summary_text = summary['text']

    summary_data = {
        'location': location,
        'summary': summary_text
    }

    with open('summary_news.json', 'w') as file_save:
        json.dump(summary_data, file_save, indent=4)

    print("Summary has been saved to summary_news.json")

if __name__ == "__main__":
    
    location = input("enter the location: ")
    period = input("Enter the period: ")
    
    get_news(location, period)
