import requests
from flask import Flask

app = Flask(__name__)

headers = {
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
    "X-RapidAPI-Key": ""
}


def search_location(query):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

    querystring = {
        "name": query,
        "locale": "en-gb"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()[0]


def search_hotel(dest_id, dest_type):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    querystring = {
        "dest_id": dest_id,
        "dest_type": dest_type,
        "adults_number": "2",
        "checkin_date": "2024-09-14",
        "checkout_date": "2024-09-15",
        "order_by": "popularity",
        "filter_by_currency": "EUR",
        "room_number": "1",
        "locale": "en-gb",
        "units": "metric",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json().get("result")[:3]


@app.route("/search/<query>", methods=["GET"])
def search(query):
    result = search_location(query)
    return search_hotel(result.get("dest_id"), result.get("dest_type"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)