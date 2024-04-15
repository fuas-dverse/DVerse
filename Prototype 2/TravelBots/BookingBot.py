import requests
import spacy

def search_hotels(user_input):
    headers = {
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
        "X-RapidAPI-Key": "0c95a1450amsh3509f87e8c01454p150fd2jsn55ba72695e6f",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    nlp = spacy.load("en_core_web_sm")

    def extract_city(input_text):
        doc = nlp(input_text)
        cities = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
        return cities[0] if cities else None

    def search_location(city):
        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
        querystring = {
            "name": city,
            "locale": "en-gb"
        }
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()[0] if response.status_code == 200 else None

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
        first_results = response.json().get("result")[:3]

        results = []
        for hotel in first_results:
            results.append({
                "name": hotel.get("hotel_name"),
                "address": hotel.get("address"),
                "rating": hotel.get("review_score_word"),
                "price": hotel.get("min_total_price"),
                "url": hotel.get("url"),
                "image": hotel.get("main_photo_url")
            })
        return results

    city = extract_city(user_input)
    if city:
        print(f"Searching hotels in {city}...")

        try:
            location_data = search_location(city)
            hotels = search_hotel(location_data["dest_id"], location_data["dest_type"])
            if hotels:
                for hotel in hotels:
                    print(hotel)  # Print out hotel details
            else:
                print("No hotels found.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    else:
        print("No city mentioned in your input.")

# # Test the function with user input
# while True:
#      user_input = input("Enter your desired location or 'exit' to quit: ")
#      if user_input.lower() == "exit":
#           break
#      search_hotels(user_input)