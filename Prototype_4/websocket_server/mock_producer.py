import json

from kafka_manager.kafka_manager import KafkaManager

if __name__ == "__main__":
    kafka_manager = KafkaManager()
    message = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "@type": "Object",
        "actor": "agent",
        "content": {
            "type": "text",
            "value": "Blah blah blah",
        },
        "chatId": "3xgprmypgweag8c01ub7cs",
    }
    message = json.dumps(message)
    kafka_manager.producer.produce("google-search.output",  message)
    kafka_manager.producer.flush()
