from confluent_kafka import Producer, Consumer
from transformers import pipeline
import threading
import json


class ConversationContextManager:
    def __init__(self, bootstrap_servers, message_topic, router):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.consumer = Consumer({'bootstrap.servers': bootstrap_servers, 'group.id': 'nlp_group',
                                  'auto.offset.reset': 'earliest'})
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
        self.message_topic = message_topic
        self.nlp_input_topic = self.nlp_input_topic
        self.nlp_output_topic = self.nlp_output_topic
        self.router = router

        # Subscribe to the NLP output topic
        self.consumer.subscribe([self.nlp_output_topic])
        threading.Thread(target=self._consume_nlp_output).start()

    def classify_and_route(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        classified_message = {"message": message, "intent": output["labels"][0]}
        self.router.route_message(output["labels"][0], self.message_topic, classified_message)

        # Send the classified message to the NLP_output topic
        self.producer.produce(self.nlp_output_topic, value=json.dumps(classified_message).encode('utf-8'))
        self.producer.flush()

        return classified_message

    def _consume_nlp_output(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            message = json.loads(msg.value().decode('utf-8'))
            intent = message['intent']
            user_input = message['message']
            response = self.router.process_intent(user_input, intent)
            self.router.route_message(intent, self.nlp_output_topic, response)

