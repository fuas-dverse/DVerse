from googleapiclient.discovery import build

# Google Custom Search API key and search engine ID
API_KEY = 'AIzaSyA58b1fAHcNRfGynXNDbJf2bGPXzAaJcsY'
SEARCH_ENGINE_ID = '37324418f13494ff8'

# Function to search on Google and return the first 5 links
def search_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
        num=5,  # Number of results to retrieve
    ).execute()
    return res['items']
