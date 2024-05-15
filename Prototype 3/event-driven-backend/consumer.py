import os
from confluent_kafka import Consumer, KafkaException, KafkaError
import json

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from dotenv import load_dotenv
import requests

load_dotenv()


class KafkaConsumer:
    def __init__(self, conf, topics):
        self.consumer = Consumer(conf)
        self.admin_client = AdminClient({'bootstrap.servers': conf['bootstrap.servers']})
        self.topics = topics
        self.running = True
        self.ensure_topics_exist()
        self.consumer.subscribe(topics)

    def ensure_topics_exist(self):
        existing_topics = self.admin_client.list_topics(timeout=10).topics
        new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in self.topics if
                      topic not in existing_topics]
        if new_topics:
            fs = self.admin_client.create_topics(new_topics)
            for topic, f in fs.items():
                try:
                    f.result()  # The result itself is None
                    print(f"Topic {topic} created successfully")
                except Exception as e:
                    print(f"Failed to create topic {topic}: {e}")

    def classify_and_process_message(self, msg):
        try:
            message = json.loads(msg.value().decode('utf-8'))
            if msg.topic() == 'create_note':
                content = message.get('object', {}).get('content', '')
                classification = self.classify_content(content)
                self.create_object(content, classification)
            elif msg.topic() == 'create_object':
                print(f"Received create_object message: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def classify_content(self, content):
        if 'travel' in content.lower():
            classification = 'travel'
            print(f"Classified as travel note: {content}")
        elif 'food' in content.lower():
            classification = 'food'
            print(f"Classified as food note: {content}")
        else:
            classification = None
            print(f"Received note: {content}")
        return classification

    def create_object(self, user_input, classification):
        url = f"{os.getenv('BASE_URL')}/produce"
        payload = {
            "context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "actor": "https://example.com/users/1",
            "object": {
                "type": "Object",
                "user_input": user_input,
                "classified": classification
            }
        }
        response = requests.post(url, json=payload)
        print(f"Produce Create Object Event: {response.status_code}, {response.json()}")

    def consume_loop(self):
        try:
            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                    else:
                        raise KafkaException(msg.error())
                else:
                    self.classify_and_process_message(msg)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


if __name__ == "__main__":
    conf = {
        'bootstrap.servers': 'host.docker.internal:9092',
        'group.id': 'DVerse',
        'auto.offset.reset': 'earliest',
    }
    topics = ['create_note', 'create_object']
    kafka_consumer = KafkaConsumer(conf, topics)
    kafka_consumer.consume_loop()
