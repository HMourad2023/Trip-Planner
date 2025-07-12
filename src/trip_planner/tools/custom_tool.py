from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import json
import requests
from crewai import LLM,Task,Agent
from unstructured.partition.html import partition_html

class WebsiteInput(BaseModel):
    """Input schema for MyCustomTool."""
    website: str = Field(..., description="The website URL to scrape.")

class BrowserTools(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> str:
        try:
            # Get API key from environment variable
            api_key = os.environ.get("BROWSERLESS_API_KEY", "")
            if not api_key:
                return "Error: BROWSERLESS_API_KEY environment variable is not set."

            # Prepare the API request
            url = f"https://chrome.browserless.io/content?token={api_key}"
            payload = json.dumps({"url": website})
            headers = {
                'cache-control': 'no-cache',
                'content-type': 'application/json'
            }

            # Make the request to Browserless
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                return f"Error: Failed to fetch website content. Status code: {response.status_code}"

            # Parse the HTML content
            elements = partition_html(text=response.text)
            content = "\n\n".join([str(el) for el in elements])

            # Split content into chunks if needed
            content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summaries = []

            # Load your preferred LLM
            llm = LLM(model="gemini/gemini-2.0-flash")

            # Summarize each chunk
            for chunk in content_chunks:
                agent = Agent(
                    role='Principal Researcher',
                    goal='Do amazing researches and summaries based on the content you are working with',
                    backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                    allow_delegation=False,
                    llm=llm
                )
                task = Task(
                    description=f'Analyze and summarize the content below. Return only the summary.\n\nCONTENT:\n{chunk}',
                    agent=agent
                )
                summary = task.execute()
                summaries.append(summary)

            return "\n\n".join(summaries)

        except Exception as e:
            return f"Error while processing website: {str(e)}"

    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented")
    

class SearchQuery(BaseModel):
    query: str = Field(..., description="The search query to look up")

class SearchTools(BaseTool):
    name: str = "Search the internet"
    description: str = "Useful to search the internet about a given topic and return relevant results"
    args_schema: type[BaseModel] = SearchQuery

    def _run(self, query: str) -> str:
        try:
            top_result_to_return = 4
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query})
            headers = {
                'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
                'content-type': 'application/json'
            }

            if not headers['X-API-KEY']:
                return "Error: SERPER_API_KEY environment variable is not set."

            response = requests.post(url, headers=headers, data=payload)
            
            if response.status_code != 200:
                return f"Error: Search API request failed. Status code: {response.status_code}"
            
            data = response.json()
            if 'organic' not in data:
                return "No results found or API error occurred."
            
            results = data['organic']
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", 
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", 
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue
            return '\n'.join(string) if string else "No valid results found"
        except Exception as e:
            return f"Error during search: {str(e)}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not implemented")


class CalculationInput(BaseModel):
    operation: str = Field(..., description="The mathematical expression to evaluate")

class CalculatorTools(BaseTool):
    name: str = "Make a calculation"
    description: str = """Useful to perform any mathematical calculations, 
    like sum, minus, multiplication, division, etc.
    The input should be a mathematical expression, e.g. '200*7' or '5000/2*10'"""
    args_schema: type[BaseModel] = CalculationInput

    def _run(self, operation: str) -> float:
        return eval(operation)

    async def _arun(self, operation: str) -> float:
        raise NotImplementedError("Async not implemented")
