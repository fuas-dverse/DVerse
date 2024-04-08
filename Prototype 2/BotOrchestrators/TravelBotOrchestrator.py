from confluent_kafka import Producer, Consumer
from ..TravelBots.BookingBot import search_booking

class TravelBotOrchestrator:
    def __init__(self, bootstrap_servers, group_id):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe(['travel_input'])
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def process_message(self, message):
        print("Travel Bot Orchestrator received message:", message)
        # Trigger BookingBot and process response
        search_results = search_booking(message)
        booking_response = "\n".join([f"Hotel Name: {item['entities'][0]['name']}\nURL: https://www.booking.com/search.html?dest_id={item['entities'][0]['destinationId']}&dest_type=city" for item in search_results if item['group'] == 'HOTEL_GROUP'])
        self.send_message('travel_output', booking_response)

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()

# Example usage:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    travel_bot_orchestrator = TravelBotOrchestrator(bootstrap_servers, 'travel_group')
