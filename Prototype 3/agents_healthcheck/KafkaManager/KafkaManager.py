import os
import threading
import time

from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, KafkaException, TopicPartition


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
        self.messages = []
        self.lock = threading.Lock()

    def send_message(self, topic, message, key=None):
        """
        Sends a message to a Kafka topic
        """
        self.__create_non_existing_topics(topic)

        headers = {'requestId': key}
        if isinstance(message, dict):
            message = str(message)
        self.producer.produce(topic, value=message.encode('utf-8'), headers=headers)
        self.producer.flush()
        print(f"Message sent to topic {topic}: {message}")

    def start_consuming(self, topic):
        """
        Start consuming messages from the specified topic
        """
        threading.Thread(target=self.__consume_messages, args=(topic,)).start()

    def subscribe(self, topic):
        """
        Subscribes to a Kafka topic
        """
        self.__create_non_existing_topics(topic)

    def __list_topics(self):
        """
        Lists all Kafka topics
        """
        return self.admin.list_topics().topics

    def __create_topic(self, topic, partitions=1, replication=3):
        """
        Creates a new Kafka topic
        """
        new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
        fs = self.admin.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    def __create_non_existing_topics(self, topic):
        """
        Creates the specified topics if they do not already exist
        """
        if "^" not in topic:
            if topic not in self.__list_topics():
                self.__create_topic(topic)

    def __consume_messages(self, topic):
        """
        Consumes messages from a Kafka topic and stores them
        """
        self.consumer.subscribe([topic])
        self.consumer.subscribe([topic])
        while True:
            try:
                msg = self.consumer.poll(timeout=0.1)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    elif msg.error():
                        raise KafkaException(msg.error())
                self.__store_message(msg)
            except KafkaException as e:
                print(f"Kafka error: {e}")
                self.consumer.seek(TopicPartition(topic, 0, 0))  # Reset to the beginning if there's an error

    def __store_message(self, msg):
        """
        Stores messages in the internal list
        """
        with self.lock:
            self.messages.append(msg.value().decode('utf-8'))

    def get_messages(self):
        """
        Retrieves the stored messages
        """
        with self.lock:
            messages = self.messages[:]
        return messages

    def consume_messages(self, topic, duration=5):
        """
        Consumes messages for a specific duration from a Kafka topic
        """
        self.subscribe(topic)
        self.start_consuming(topic)
        time.sleep(duration)
        return self.get_messages()
