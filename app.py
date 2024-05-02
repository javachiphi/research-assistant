import os
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup
import requests
import json
from langchain.schema import SystemMessage
from fastapi import FastAPI

load_dotenv()

brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")


#1. tool for search
def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text


#2. tool for scraping
def scrape_website(objective: str, url: str):
    print("Scraping website...")
    headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENTTTTTT:", text[:100])  # Displaying first 100 chars for brevity

        # if len(text) > 10000:
        #     output = summary(objective, text)
        #     return output
        # else:
        #     return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")
        return None 


# def test_scrape():
#     objective = "Test scraping functionality"
#     url = "https://news.ycombinator.com/item?id=32409632"  # Replace with a target URL that's safe to scrape
#     result = scrape_website(objective, url)
#     print(result)

# if __name__ == "__main__":
#     test_scrape()
    


#3. create langchain agent with the tools above 
    