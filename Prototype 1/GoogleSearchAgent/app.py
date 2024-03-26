import json

import requests
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
        query = data.get("query")
        available_festival = data["responses"][0].get("festival_results")

        if available_festival:
            response = fetch_google_results(f"Tickets {available_festival}")
        else:
            response = fetch_google_results(query)

        data["responses"].append({"google_results": response})

        next_domain = check_next_domain(data)
        headers = {'Content-Type': 'application/json'}
        requests.post(next_domain, data=json.dumps(data), headers=headers)

        return jsonify({'success': True}), 200
    else:
        return "Make a POST request to this url"


def check_next_domain(data):
    current_domain = request.base_url
    current_index = data["domains"].index(current_domain)

    if current_index + 1 < len(data["domains"]):
        next_domain = data["domains"][current_index + 1]
    else:
        next_domain = data["origin"]

    return next_domain


if __name__ == '__main__':
    app.run(port=5002, debug=True)
