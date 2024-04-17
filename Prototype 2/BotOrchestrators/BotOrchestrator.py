from confluent_kafka import Producer, Consumer


class BotOrchestrator:
    def __init__(self, bootstrap_servers, group_id, bot_type, input_topic, output_topic, search_function):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([input_topic])
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.search_function = search_function
        self.output_topic = output_topic

    def process_message(self, message):
        print(f"{self.__class__.__name__} received message:", message)
        # Trigger search function and process response
        search_results = self.search_function(message)
        formatted_response = self.format_response(search_results)
        self.send_message(self.output_topic, formatted_response)

    def format_response(self, search_results):
        raise NotImplementedError("Subclasses must implement the format_response method")

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()
