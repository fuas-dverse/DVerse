from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from googleapiclient.discovery import build

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# YouTube API key
API_KEY = ''


def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=3  # Number of results to retrieve
    )
    response = request.execute()
    return response['items']


@app.route('/search-youtube', methods=['GET'])
def search_youtube_api():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing.'}), 400

    try:
        search_results = search_youtube(query)
        videos = []
        for item in search_results:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({'title': title, 'url': video_url})
        return jsonify(videos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
