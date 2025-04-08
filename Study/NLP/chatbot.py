import requests
import ollama
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import datetime

def search_duckduckgo(query, max_results=5, region='wt-wt', safesearch='off'):
    """
    Search the web using DuckDuckGo and return a list of results.

    Parameters:
    - query (str): The search query string.
    - max_results (int): Maximum number of results to return.
    - region (str): Region code, e.g., 'wt-wt' (worldwide), 'us-en', 'uk-en'.
    - safesearch (str): Safesearch level - 'off', 'moderate', or 'strict'.

    Returns:
    - List[Dict[str, str]]: List of search result dictionaries with 'title', 'href', and 'body'.
    """
    print(f"Searching DuckDuckGo for: {query}")
    print(f"Region: {region}, SafeSearch: {safesearch}")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region=region, safesearch=safesearch):
            results.append(r)
            if len(results) >= max_results:
                break
    return results

def scrape_webpage(url, timeout=10):
    """
    Scrapes the main text content from a webpage.

    Parameters:
    - url (str): The URL of the webpage to scrape.
    - timeout (int): Request timeout in seconds.

    Returns:
    - str: Extracted text content from the page, or an error message.
    """
    print(f"Scraping URL: {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        # Try to get main content (simple strategy)
        main = soup.find('main') or soup.find('article') or soup.body
        text = main.get_text(separator='\n', strip=True)

        return text  # Optionally truncate to avoid overload
    except Exception as e:
        return f"[Error scraping {url}]: {str(e)}"

def scrape_search_results(results):
    """
    Given a list of search results, scrape each page.

    Parameters:
    - results (List[Dict]): List of search result dictionaries from DuckDuckGo.

    Returns:
    - List[Dict]: Each dict contains 'title', 'url', and 'content'.
    """
    scraped_data = []
    for result in results:
        url = result['href']
        content = scrape_webpage(url)
        scraped_data.append({
            'title': result['title'],
            'url': url,
            'content': content
        })
    return scraped_data

def summarize_all_scraped(scraped_pages, question, model='llama3.2'):
    """
    Combines all scraped page content and summarizes it into one summary.

    Parameters:
    - scraped_pages (List[Dict]): Each dict should have 'title', 'url', 'content'.
    - model (str): The Ollama model to use (e.g., 'deepseek-llm').

    Returns:
    - str: A single, unified summary.
    """
    print(f"Summarizing {len(scraped_pages)} pages using model: {model}")
    combined_text = ""
    for page in scraped_pages:
        print(f"Processing page: {page['title']}")
        # Combine title, URL, and content
        combined_text += f"\nTitle: {page['title']}\nURL: {page['url']}\n\n{page['content']}\n"
    
    print("Length of combined text:", len(combined_text))
    # Truncate to avoid overloading model
    # if len(combined_text) > 17000:
    #     combined_text = combined_text[:17000]

    prompt = (
        f"{combined_text}\n"
        "Please read the provided combined content from multiple web pages and write a single, concise, informative to answer this query:"
        f"\n{question}"
    )

    print(datetime.datetime.now())

    # print(prompt)
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    print(datetime.datetime.now())

    return response["message"]["content"]

query = "Information about the latest advancements in AI technology"
results = search_duckduckgo(query)
scraped_pages = scrape_search_results(results)
summary = summarize_all_scraped(scraped_pages, question=query)
print(summary)