import logging
from confluent_kafka import Consumer, Producer
from transformers import pipeline


class ClassifierAgent:
    def __init__(self, consumer_config, producer_config, classifier_model):
        self.consumer = Consumer(consumer_config)
        self.producer = Producer(producer_config)
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)

    def consume_messages(self, topic):
        self.consumer.subscribe([topic])
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logging.error(f"Consumer error: {message.error()}")
                continue
            self.classify_input(message.value().decode('utf-8'))

    def produce_message(self, topic, message):
        self.producer.produce(f"{topic}.input", value=message.encode('utf-8'))
        self.producer.flush()

    def classify_input(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        classified_message = {"message": message, "intent": output["labels"][0]}
        logging.info(classified_message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = ClassifierAgent(
        consumer_config={'bootstrap.servers': 'host.docker.internal:9092', 'group.id': 'classifier_agent', 'auto.offset.reset': 'earliest'},
        producer_config={'bootstrap.servers': 'host.docker.internal:9092'},
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
    )
    agent.consume_messages('classifier.input')
