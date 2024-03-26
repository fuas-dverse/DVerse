import json

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import sys

app = Flask(__name__)
socketio = SocketIO(app)

ORIGIN_URL = "http://websocket-server:5003/"
FESTIVAL_AGENT_API_URL = 'http://festival-information-agent:5000/'
YOUTUBE_AGENT_API_URL = 'http://youtube-search-agent:5001/'
GOOGLE_AGENT_API_URL = 'http://google-search-agent:5002/'


# Check if a port number is provided as a command-line argument
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Using default port 5000.")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = request.json

        socketio.emit('search_and_chat_results', data)

        return jsonify({'success': True}), 200


@socketio.on('search_and_chat')
def handle_search_and_chat(data):
    user_input = data['query']
    try:
        payload = {
            "query": user_input,
            "origin": ORIGIN_URL,
            "domains": [
                FESTIVAL_AGENT_API_URL,
                YOUTUBE_AGENT_API_URL,
                GOOGLE_AGENT_API_URL
            ]
        }
        headers = {'Content-Type': 'application/json'}

        requests.post(payload["domains"][0], data=json.dumps(payload), headers=headers)
    except Exception as e:
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    socketio.run(app, port=5003, allow_unsafe_werkzeug=True)
