import requests
import spacy

headers = {
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
    "X-RapidAPI-Key": "0c95a1450amsh3509f87e8c01454p150fd2jsn55ba72695e6f",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}


def search_hotels(self, user_input):
        """
        Extracts city name from user input and searches for hotels.

        Args:
            user_input (str): User's desired location.

        Returns:
            list or None: List of dictionaries containing hotel information or None if no city found or error occurred.
        """

        city = self.extract_city(user_input)
        if city:
            print(f"Searching hotels in {city}...")

            try:
                location_data = self.search_location(city)
                hotels = self.search_hotel(location_data["dest_id"], location_data["dest_type"])
                return hotels
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return None
        else:
            print("No city mentioned in your input.")
            return None

def extract_city(self, input_text):
    """
    Extracts the name of the city from the input text using spaCy.

     Args:
         input_text (str): User's input.

     Returns:
         str or None: Extracted city name or None if not found.
     """

    doc = self.nlp(input_text)
    cities = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
    return cities[0] if cities else None

def search_location(self, city):
        """
        Searches for location information using Booking.com API.

        Args:
            city (str): City name.

        Returns:
            dict or None: Location information from API or None if error occurred.
        """

        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

        querystring = {
            "name": city,
            "locale": "en-gb"
        }

        response = requests.get(url, headers=self.headers, params=querystring)
        return response.json()[0] if response.status_code == 200 else None

def search_hotel(self, dest_id, dest_type):
        """
        Searches for hotels in the specified location using Booking.com API.

        Args:
            dest_id (str): Destination ID from location search.
            dest_type (str): Destination type from location search.

        Returns:
            list or None: List of dictionaries containing hotel information or None if error occurred.
        """

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

        response = requests.get(url, headers=self.headers, params=querystring)
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


