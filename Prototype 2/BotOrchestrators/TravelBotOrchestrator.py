from confluent_kafka import Producer, Consumer
from TravelBots import search_hotel
from LanguageLearningBots import search_google
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
        google_results = search_google(message)
        hotel_results = search_hotel(message)
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
        formatted_response = "\n".join([f"Hotel Name: {item['entities'][0]['name']}\nURL: https://www.booking.com/search.html?dest_id={item['entities'][0]['destinationId']}&dest_type=city" for item in search_results if item['group'] == 'HOTEL_GROUP'])
        return formatted_response
    
    def format_response(self, search_results):
        google_results, hotel_results = search_results
        google_response = "\n".join([f"Title: {item['title']}\nURL: {item['link']}" for item in google_results])
        hotel_response = "\n".join([f"Hotel Name: {item['entities'][0]['name']}\nURL: https://www.booking.com/search.html?dest_id={item['entities'][0]['destinationId']}&dest_type=city" for item in search_results if item['group'] == 'HOTEL_GROUP'])
        return google_response + "\n" + hotel_response

# Example:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    travel_bot_orchestrator = TravelBotOrchestrator(bootstrap_servers, 'travel_group')
