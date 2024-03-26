import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from googleapiclient.discovery import build

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

load_dotenv()

# YouTube API key
API_KEY = os.environ.get('API_KEY')


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


@app.route('/', methods=['POST'])
def search_youtube_api():
    data = request.json
    query = data["query"]
    available_festival = data["responses"][0].get("festival_results")

    if available_festival:
        query = f"After movie {available_festival}"

    try:
        search_results = search_youtube(query)
        videos = []
        for item in search_results:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({'title': title, 'url': video_url})

        data['responses'].append({'youtube_results': videos})

        next_domain = check_next_domain(data)
        headers = {'Content-Type': 'application/json'}
        requests.post(next_domain, data=json.dumps(data), headers=headers)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def check_next_domain(data):
    current_domain = request.base_url
    current_index = data["domains"].index(current_domain)

    if current_index + 1 < len(data["domains"]):
        next_domain = data["domains"][current_index + 1]
    else:
        next_domain = data["origin"]

    return next_domain


if __name__ == '__main__':
    app.run(port=5001, debug=True)
