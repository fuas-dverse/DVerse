import json

import requests
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from kafka_manager.kafka_manager import KafkaManager


class ClassifierAgent:
    def __init__(self, classifier_model,  nlp_input_topic, nlp_output_topic):
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)
        self.kafka_manager = KafkaManager()
        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.llm = ChatOpenAI()
        self.consume_messages(self.nlp_input_topic)

    def consume_messages(self, topic):
        self.kafka_manager.subscribe(topic, self.classify_input)
        self.kafka_manager.start_consuming()

    def produce_message(self, topic, message):
        self.kafka_manager.send_message(f"{topic}.input", message.encode('utf-8'))

    def classify_input(self, message):
        decoded_message = message.value().decode('utf-8')

        output = self.classifier(decoded_message, ["language", "travel"], multi_label=False)
        classified_message = {"message": decoded_message, "intent": output["labels"][0]}

        response = self.process_intent(decoded_message, output["labels"][0])
        print(response)

        # Send the classified message to the nlp_output topic
        self.kafka_manager.send_message(self.nlp_output_topic, {"classifier-agent": str(json.dumps(classified_message))})

    def process_intent(self, user_input, intent):
        bots_info = requests.get("https://localhost:8000/" + intent).json()
        print(bots_info)

        # response = self.generate_response_with_langchain(user_input, bots_info)
        # print(response)
        # return response

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
    agent = ClassifierAgent(
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp.input",
        nlp_output_topic="nlp.output"
    )


