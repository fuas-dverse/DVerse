from confluent_kafka import Producer
from transformers import pipeline


class ConversationContextManager:
    def __init__(self, bootstrap_servers, message_topic, router):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
        self.message_topic = message_topic
        self.router = router

    def classify_and_route(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        classified_message = {"message": message, "intent": output["labels"][0]}
        self.router.route_message(output["labels"][0], self.message_topic, classified_message)
        return classified_message
