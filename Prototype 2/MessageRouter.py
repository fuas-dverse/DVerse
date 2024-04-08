from confluent_kafka import Producer, Consumer

class MessageRouter:
    def __init__(self, bootstrap_servers):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()

    def subscribe(self, topic, group_id, callback):
        consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe([topic])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            callback(msg.value().decode('utf-8'))

# Example (to be checked if works)
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    message_router = MessageRouter(bootstrap_servers)
