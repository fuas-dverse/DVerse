from googlesearch import search
from flask import Flask, request, jsonify

app = Flask(__name__)


def fetch_google_results(query):
    try:
        return list(search(query, num_results=1))
    except Exception as e:
        print("An error occurred:", e)
        return []


@app.route('/', methods=['GET', 'POST'])
def get_response():
    if request.method == 'POST':
        data = request.json
        query = data['query']

        response = fetch_google_results(query)

        return jsonify({"response": response})
    else:
        return "Make a POST request to this url"


if __name__ == '__main__':
    app.run(port=5002, debug=True)
