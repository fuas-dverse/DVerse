from confluent_kafka import Producer, Consumer
from LanguageLearningBots import search_google
from TravelBots.BookingBot import search_location, search_hotel  # Importing functions from BookingBot
from .BotOrchestrator import BotOrchestrator

class TravelBotOrchestrator(BotOrchestrator):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            bot_type='TravelBot',
            input_topic='travel_input',
            output_topic='travel_output',
            search_function=self.search_travel
        )

    def search_travel(self, message):
        user_input = message  # Assuming message contains user input
        google_results = search_google(user_input)
       # hotel_results = self.search_hotels(user_input)  # Using search_hotels method of TravelBotOrchestrator
        return google_results
    #, hotel_results
    
    def consume(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            self.process_message(msg.value().decode('utf-8'))

    def search_hotels(self, user_input):
        city = self.extract_city(user_input)
        if city:
            try:
                location_data = search_location(city)
                hotels = search_hotel(location_data["dest_id"], location_data["dest_type"])
                return hotels
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
        else:
            print("No city mentioned in your input.")
            return None

    def format_response(self, search_results):
        google_results, hotel_results = search_results
        google_response = "\n".join([f"Title: {item['title']}\nURL: {item['link']}" for item in google_results])
        #3hotel_response = "\n".join([f"Hotel Name: {item['name']}\nAddress: {item['address']}\nRating: {item['rating']}\nPrice: {item['price']} EUR per night\nURL: {item['url']}" for item in hotel_results]) if hotel_results else "No hotels found."
        return google_response 
    #+ "\n" + hotel_response

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

# Example:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    travel_bot_orchestrator = TravelBotOrchestrator(bootstrap_servers, 'travel_group')
