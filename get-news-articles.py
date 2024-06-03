'''
Documention for GNews: https://github.com/ranahaani/GNews/blob/master/README.md

in get_News(location,period) 
location can be Manglaore,bangalore etc..
for period it can be :
these:
 - h = hours (eg: 12h)
 - d = days (eg: 7d)
 - m = months (eg: 6m)
 - y = years (eg: 1y)

'''


import json
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass

# Function to scrape content from a given URL
def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.text for p in paragraphs])
    return content

def get_News(location,period):
    # Get environmental news for a given location
    location = location
    google_news = GNews(max_results=5,period=period)
    news_items = google_news.get_news(f'{location}: environmental')

    # Extract URLs and scrape content
    all_contents = ""
    for item in news_items:
        url = item['url']
        content = scrape_content(url)
        all_contents += content + "\n"

    # Provide your Google API Key
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

    # Initialize the Gemini AI model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    # Generate a summary for all concatenated contents
    result = llm.invoke(f"Summarize the following news content which should include the promises made,any percentage mentioned,date of publish,any kind of political party Name mentioned:\n{all_contents}")
    summary = result.content

    # Save the summary to a JSON file
    summary_data = {
        'location': location,
        'summary': summary
    }

    with open('summary_news.json', 'w') as f:
        json.dump(summary_data, f, indent=4)

    print("Summary has been saved to summary_news.json")


if __name__ == "__main__":
    get_News('Mangalore','1y')