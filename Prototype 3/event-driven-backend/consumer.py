from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import os

# Kafka configuration
conf = {
    'bootstrap.servers': 'host.docker.internal:9092',  # Replace with your Kafka broker(s)
    'group.id': 'my_group',  # Consumer group ID
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

            # TODO: Implement a better classification method
            if 'travel' in content.lower():
                print(f"Classified as travel note: {content}")
                # Produce to another topic or perform other actions
            else:
                print(f"Received note: {content}")
        elif msg.topic() == 'create_object':
            # Handle create_object messages
            print(f"Received create_object message: {message}")
    except Exception as e:
        print(f"Error processing message: {e}")


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
