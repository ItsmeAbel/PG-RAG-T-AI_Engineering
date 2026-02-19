import requests

def get_top_stories():
    #uses this free public api to get news
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": 'RAG "AI Engineering"',
        "tags": "story",
        "hitsPerPage": 10
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status() # Good practice: raises an error if the API is down
    
    hits = response.json().get('hits', [])
    
    #Format for LLM with a fallback if 'url' is missing
    # We use .get('url', 'No URL provided') to prevent crashes
    context = "\n".join([
        f"Title: {h['title']} - URL: {h.get('url') or 'https://news.ycombinator.com/item?id=' + h['objectID']}" 
        for h in hits
    ])

    return context