from googleapiclient.discovery import build

# Google Custom Search API key and search engine ID
API_KEY = 'API_KEY'
SEARCH_ENGINE_ID = 'searchid'

# Function to search on Google and return the first 5 links
def search_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
        num=5,  # Number of results to retrieve
    ).execute()
    return res['items']

# Example
user_input = "holiday recommendations in Europe"
search_results = search_google(user_input)

# Print titles and URLs of search results
for item in search_results:
    title = item['title']
    link = item['link']
    print(f"Title: {title}")
    print(f"URL: {link}")
    print()