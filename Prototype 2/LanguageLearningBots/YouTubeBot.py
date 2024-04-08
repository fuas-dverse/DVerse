from googleapiclient.discovery import build

# YouTube API key
API_KEY = 'api-key'

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

# Example
user_input = "holiday recommendations in Europe"
search_results = search_youtube(user_input)

# Print video titles and URLs
for item in search_results:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    print(f"Title: {title}")
    print(f"URL: {video_url}")
    print()