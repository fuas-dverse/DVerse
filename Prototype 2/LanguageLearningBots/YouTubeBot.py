from googleapiclient.discovery import build

# YouTube API key
API_KEY = 'AIzaSyBnaSEPWFTrvahe-4JTpT1rz06w1avVyxo'

# Function to search for videos on YouTube
def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=5  # Number of results to retrieve
    )
    response = request.execute()
    return response['items']