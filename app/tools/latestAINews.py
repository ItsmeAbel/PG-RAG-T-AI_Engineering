import requests

def get_top_stories():
    #uses a free public api to get top headlines
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": 'RAG "AI Engineering"',
        "tags": "story",
        "hitsPerPage": 15
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status() # raises an error if the API is down
    
    hits = response.json().get('hits', [])
    
    #Format for LLM with a fallback if url is missing
    # .get('url', 'No URL provided') can be used to prevent crashes
    context = "\n".join([
        f"Title: {h['title']} - URL: {h.get('url') or 'https://news.ycombinator.com/item?id=' + h['objectID']}" 
        for h in hits
    ])

    return context