import nltk
import requests
import locationtagger


def download_nltk_packages():
    packages = ['maxent_ne_chunker', 'words', 'treebank', 'maxent_treebank_pos_tagger', 'punkt',
                'averaged_perceptron_tagger']
    for package in packages:
        try:
            nltk.data.find(package)
        except LookupError:
            nltk.downloader.download(package)


def search_hotels(user_input):
    download_nltk_packages()

    headers = {
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
        "X-RapidAPI-Key": "0c95a1450amsh3509f87e8c01454p150fd2jsn55ba72695e6f",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    city = locationtagger.find_locations(text=user_input.title()).cities[0] if locationtagger.find_locations(
        text=user_input.title()).cities else None
    if city:
        print(f"Searching hotels in {city}...")
        try:
            location_data = requests.get("https://booking-com.p.rapidapi.com/v1/hotels/locations", headers=headers,
                                         params={"name": city, "locale": "en-gb"}).json()[0]
            hotels = requests.get("https://booking-com.p.rapidapi.com/v1/hotels/search", headers=headers, params={
                "dest_id": location_data["dest_id"],
                "dest_type": location_data["dest_type"],
                "adults_number": "2",
                "checkin_date": "2024-09-14",
                "checkout_date": "2024-09-15",
                "order_by": "popularity",
                "filter_by_currency": "EUR",
                "room_number": "1",
                "locale": "en-gb",
                "units": "metric",
            }).json().get("result")[:3]
            return [{"name": hotel.get("hotel_name"), "address": hotel.get("address"),
                     "rating": hotel.get("review_score_word"), "price": hotel.get("min_total_price"),
                     "url": hotel.get("url"), "image": hotel.get("main_photo_url")} for hotel in hotels]
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    else:
        print("No city found in the input.")

# if __name__ == "__main__":
#     while True:
#         user_input = input("Enter your desired location or 'exit' to quit: ")
#         if user_input.lower() == "exit":
#             break
#         print(search_hotels(user_input))
