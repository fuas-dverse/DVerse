import json

from BotOrchestrators.BotOrchestrator import BotOrchestrator
from LanguageLearningBots import search_google
from TravelBots.BookingBot import search_hotels


class TravelBotOrchestrator(BotOrchestrator):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            bot_type='TravelBot',
            input_topic='travel_input',
            output_topic='topic_output',
            search_function=self.search_travel
        )

    def search_travel(self, message):
        google_results = search_google(message)
        hotel_results = search_hotels(message)  # Using search_hotels method of TravelBotOrchestrator
        return google_results, hotel_results

    def consume(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            self.process_message(msg.value().decode('utf-8'))

    def format_response(self, search_results):
        google_results, hotel_results = search_results
        google_response = [{"Title": item['title'], "URL": item['link']} for item in google_results]
        hotel_response = [{"Title": item['name'], "Address": item['address'], "Rating": item['rating'],
                           "Price": f"{item['price']} EUR per night", "URL": item['url']} for item in
                          hotel_results] if hotel_results else [{"Message": "No hotels found."}]
        response = {"GoogleResults": google_response, "HotelResults": hotel_response}
        return json.dumps(response)


# Example:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    travel_bot_orchestrator = TravelBotOrchestrator(bootstrap_servers, 'travel_group')
    travel_bot_orchestrator.consume()
