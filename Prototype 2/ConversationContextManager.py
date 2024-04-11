from transformers import pipeline
from confluent_kafka import Producer, Consumer

class ConversationContextManager:
    def __init__(self, bootstrap_servers, message_topic, router):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
        self.message_topic = message_topic
        self.router = router

    def classify_and_route(self, message):
        hypothesis_template = "This text is about {}"
        classes_verbalized = ["language", "travel"]
        output = self.classifier(message, classes_verbalized, hypothesis_template=hypothesis_template, multi_label=False)
        predicted_label = output["labels"][0]

        # Combine message and classification for routing
        classified_message = {"message": message, "intent": predicted_label}

        # Send the classified message to the MessageRouter
        self.router.route_message(predicted_label, self.message_topic, classified_message)

        # Return the classified message (for MessageRouter)
        return classified_message