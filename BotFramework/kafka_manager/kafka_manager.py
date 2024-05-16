import os
import threading
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from dotenv import load_dotenv

load_dotenv()


class KafkaManager:
    def __init__(self, group_id="default"):
        config = {
            'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVER"),
            'security.protocol': os.environ.get("KAFKA_SECURITY_PROTOCOL"),
            'sasl.mechanisms': os.environ.get("KAFKA_SASL_MECHANISMS"),
            'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
            'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
        }

        self.admin = AdminClient(config)
        self.producer = Producer(config)

        config['group.id'] = group_id
        config['auto.offset.reset'] = 'earliest'

        self.consumer = Consumer(config)
        self.subscriptions = {}

    def route_message(self, label, topic, message):
        headers = {'requestId': None}
        if label == "language":
            self.send_message('language_input', message)
        elif label == "travel":
            self.send_message('travel_input', message)

    def send_message(self, topic, message, key=None):
        headers = {'requestId': key}
        if isinstance(message, dict):  # Check if message is a dictionary
            message = str(message)  # Convert dictionary to string
        self.producer.produce(topic, value=message.encode('utf-8'), headers=headers)
        self.producer.flush()

    def start_consuming(self):
        # Start consuming messages
        for topic, callback in self.subscriptions.items():
            threading.Thread(target=self._consume_messages, args=(topic, callback)).start()

    def subscribe(self, topic, callback):
        if topic not in self._list_topics():
            self._create_topic(topic)

        # Add the callback to the subscriptions dictionary
        self.subscriptions[topic] = callback

    def _list_topics(self):
        return self.admin.list_topics().topics

    def _create_topic(self, topic, partitions=1, replication=1):
        new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
        fs = self.admin.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    def _delete_topic(self, topic):
        fs = self.admin.delete_topics([topic])
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} deleted")
            except Exception as e:
                print(f"Failed to delete topic {topic}: {e}")

    def _consume_messages(self, topic, callback):
        self.consumer.subscribe([topic])
        while True:
            print("Polling")
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            callback(msg)
