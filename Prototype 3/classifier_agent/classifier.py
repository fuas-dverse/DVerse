import logging
from confluent_kafka import Consumer, Producer
from transformers import pipeline
import threading
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from Milvus.DatabaseManager import DatabaseManager
from websocket_server.kafka_manager.kafka_manager import KafkaManager


class ClassifierAgent:
    def __init__(self, consumer_config, producer_config, classifier_model,  nlp_input_topic, nlp_output_topic):
        self.consumer = Consumer(consumer_config)
        self.producer = Producer(producer_config)
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)

        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.llm = ChatOpenAI()
        self.db_manager = DatabaseManager()

        # Subscribe to the NLP output topic
        self.consumer.subscribe([self.nlp_output_topic])
        threading.Thread(target=self.consume_nlp_output).start()

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

        # Send the classified message to the nlp_output topic
        self.producer.produce(self.nlp_output_topic, value=json.dumps(classified_message).encode('utf-8'))
        self.producer.flush()

    def consume_nlp_output(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            message = json.loads(msg.value().decode('utf-8'))
            intent = message['intent']
            user_input = message['message']
            response = self.process_intent(user_input, intent)

            print(response)

    # Find relevant bots based on the intent using LLM

    def process_intent(self, user_input, intent):
        bots_info = self.db_manager.get_relevant_bots(intent)
        response = self.generate_response_with_langchain(user_input, bots_info)
        return response

    def generate_response_with_langchain(self, user_input, bots_info):
        context = " ".join([f"{bot['name']}: {bot['description']} ({bot['output_format']})" for bot in bots_info])
        prompt = ChatPromptTemplate.from_template(
            """
            Answer based on the following context: {context}. What steps need to be made in order to respond to: {user_input}?
            """
        )

        chain = (
            RunnableParallel({
                "context": str,
                "user_input": RunnablePassthrough()
            })
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke({
            "context": context,
            "user_input": user_input,
        })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = ClassifierAgent(
        consumer_config={'bootstrap.servers': 'host.docker.internal:9092', 'group.id': 'classifier_agent', 'auto.offset.reset': 'earliest'},
        producer_config={'bootstrap.servers': 'host.docker.internal:9092'},
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp_input_topic",
        nlp_output_topic="nlp_output_topic"
    )


