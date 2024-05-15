import os

from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from dotenv import load_dotenv
import requests

load_dotenv()

# Kafka configuration
conf = {
    'bootstrap.servers': 'host.docker.internal:9092',  # Replace with your Kafka broker(s)
    'group.id': 'DVerse',  # Consumer group ID
    'auto.offset.reset': 'earliest',  # Start reading from the earliest message
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to multiple topics
topics = ['create_note', 'create_object']  # Replace with your topic names
consumer.subscribe(topics)


# Function to classify and process messages
def classify_and_process_message(msg):
    try:
        message = json.loads(msg.value().decode('utf-8'))
        if msg.topic() == 'create_note':
            # Perform classification based on the note content
            content = message.get('object', {}).get('content', '')
            classification = None
            # TODO: Implement a better classification method
            if 'travel' in content.lower():
                classification = 'travel'
                print(f"Classified as travel note: {content}")
            elif 'food' in content.lower():
                classification = 'food'
                print(f"Classified as food note: {content}")
            else:
                print(f"Received note: {content}")

            create_object(content, classification) # Create an object based on the classification

        elif msg.topic() == 'create_object':
            # Handle create_object messages
            print(f"Received create_object message: {message}")
    except Exception as e:
        print(f"Error processing message: {e}")


def create_object(user_input, classification):
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


# Function to handle consumed messages
def consume_loop(consumer):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process the consumed message
                classify_and_process_message(msg)

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer to commit final offsets and clean up resources
        consumer.close()


# Start the consumer loop
consume_loop(consumer)
