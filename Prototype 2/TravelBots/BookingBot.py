import requests

def search_booking(query):
    url = "https://hotels4.p.rapidapi.com/locations/search"

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "a31f31df88msh1c43741e15ac2e1p1816b5jsn5a1e8ede963e"
    }

    params = {
        "query": query,
        "locale": "en_US"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data['suggestions']

# Example
user_input = "Paris, France"
search_results = search_booking(user_input)

# Print hotel names and URLs
for item in search_results:
    if item['group'] == 'HOTEL_GROUP':
        hotel_name = item['entities'][0]['name']
        hotel_id = item['entities'][0]['destinationId']
        hotel_url = f"https://www.booking.com/search.html?dest_id={hotel_id}&dest_type=city"
        print(f"Hotel Name: {hotel_name}")
        print(f"URL: {hotel_url}")
        print()
