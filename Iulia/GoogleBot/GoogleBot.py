from googleapiclient.discovery import build
from flask import Flask, app, request, jsonify
from flask_socketio import SocketIO, emit
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Default port number
PORT = 5003

# Check if a port number is provided as a command-line argument
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Using default port 5000.")

# Google Custom Search API key and search engine ID
API_KEY = 'YOUR_GOOGLE_CSE_API_KEY'
SEARCH_ENGINE_ID = 'YOUR_SERARCH_ENGINE_ID'

def search_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
        num=5,  # Number of results to retrieve
    ).execute()
    return res['items']

@app.route('/search-google', methods=['GET'])
def search_google_api():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing.'}), 400

    try:
        search_results = search_google(query)
        links = []
        for item in search_results:
            title = item['title']
            link = item['link']
            links.append({'title': title, 'link': link})
        return jsonify(links), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=PORT, debug=True)