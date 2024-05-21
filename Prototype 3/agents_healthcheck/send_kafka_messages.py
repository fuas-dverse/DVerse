from confluent_kafka import Producer
import os
from dotenv import load_dotenv

load_dotenv()


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


p = Producer({
    'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVER"),
    'security.protocol': os.environ.get("KAFKA_SECURITY_PROTOCOL"),
    'sasl.mechanisms': os.environ.get("KAFKA_SASL_MECHANISMS"),
    'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
    'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
})

topic = os.environ.get("KAFKA_TOPIC")

for i in range(10):
    key = f"agent-{i}"
    value = f"message from {key}"
    p.produce(topic, key=key, value=value, callback=delivery_report)

p.flush()
