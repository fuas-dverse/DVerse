from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import threading
import json
import os


class KafkaClient:
    def __init__(self, brokers):
        self.brokers = brokers
        self.producer = Producer({'bootstrap.servers': self.brokers})
        self.consumer = Consumer({
            'bootstrap.servers': self.brokers,
            'group.id': 'DVerse',
            'auto.offset.reset': 'earliest'
        })
        self.consumer_thread = None
        self.running = False

    def produce(self, topic, key, value):
        try:
            self.producer.produce(topic, key=key, value=value)
            self.producer.flush()
        except KafkaException as e:
            print(f"Failed to produce message: {e}")

    def consume(self, topic, callback):
        self.consumer.subscribe([topic])
        while self.running:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    continue
            callback(msg.key().decode('utf-8'), json.loads(msg.value().decode('utf-8')))

    def start_consumer(self, topic, callback):
        if not self.consumer_thread:
            self.running = True
            self.consumer_thread = threading.Thread(target=self.consume, args=(topic, callback))
            self.consumer_thread.start()

    def stop_consumer(self):
        self.running = False
        if self.consumer_thread:
            self.consumer_thread.join()
            self.consumer_thread = None

    def close(self):
        self.stop_consumer()
        self.consumer.close()
