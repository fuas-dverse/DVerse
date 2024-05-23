import os
import threading
import time
from confluent_kafka import Consumer, KafkaException
from queue import Queue
from dotenv import load_dotenv

load_dotenv()

# In-memory cache to store messages
message_cache = Queue()


class KafkaConsumerThread(threading.Thread):
    def __init__(self, group_id="default"):
        super().__init__()
        self.running = True
        config = {
            'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVER"),
            'security.protocol': os.environ.get("KAFKA_SECURITY_PROTOCOL"),
            'sasl.mechanisms': os.environ.get("KAFKA_SASL_MECHANISMS"),
            'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
            'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(config)

    def run(self):
        self.consumer.subscribe(['agents.status'])
        while self.running:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    continue
            message_cache.put(msg.value().decode('utf-8'))

    def stop(self):
        self.running = False
        self.consumer.close()
