import json

from kafka_manager.kafka_manager import KafkaManager

if __name__ == "__main__":
    kafka_manager = KafkaManager()
    message = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "@type": "Note",
        "actor": "user",
        "content": {
            "type": "text",
            "value": "I want to book a hotel in spain",
        },
        "chatid": "kqrfo5y4xjh6ucd2vyalyk",
    }
    message = json.dumps(message)
    kafka_manager.producer.produce("google-search.output",  message)
    kafka_manager.producer.flush()
