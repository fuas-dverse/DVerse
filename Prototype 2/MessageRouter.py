from confluent_kafka import Producer, Consumer


class MessageRouter:
    def __init__(self, server):
        self.producer = Producer({
            'bootstrap.servers': server
        })

        self.consumer = Consumer({
            'bootstrap.servers': server,
            'group.id': 'group',
            'auto.offset.reset': 'earliest'
        })

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()

    def subscribe(self, topic, callback):
        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            callback(msg.value().decode('utf-8'))


if __name__ == "__main__":
    message_router = MessageRouter("host.docker.internal:9092")
    message_router.send_message("test", "Hello, World!")
    message_router.subscribe("test", lambda x: print(x))
