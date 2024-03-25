from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

YOUTUBE_BOT_API_URL = 'http://localhost:5000/search-youtube'
GOOGLE_BOT_API_URL = 'http://localhost:5003/search-google'

# Default port number
PORT = 5002

# Check if a port number is provided as a command-line argument
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Using default port 5000.")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('search_and_chat')
def handle_search_and_chat(data):
    user_input = data['query']
    try:
        youtube_response = requests.get(YOUTUBE_BOT_API_URL, params={'query': user_input})
        google_response = requests.get(GOOGLE_BOT_API_URL, params={'query': user_input})

        if youtube_response.status_code == 200 and google_response.status_code == 200:
            youtube_results = youtube_response.json()
            google_results = google_response.json()
            emit('search_and_chat_results', {'youtube_results': youtube_results, 'google_results': google_results})
        else:
            emit('error', {'message': 'Failed to fetch results from one or both bots.'})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app,port=PORT, debug=True)
