import json
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint
from transformers import pipeline

from kafka_manager.kafka_manager import KafkaManager


class ClassifierAgent:
    def __init__(self, classifier_model, nlp_input_topic, nlp_output_topic):
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)
        self.kafka_manager = KafkaManager()
        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.consume_messages(self.nlp_input_topic)

        self.model = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="text-generation",
            temperature=0.8,
        )

    def consume_messages(self, topic):
        self.kafka_manager.subscribe(topic, self.classify_input)
        self.kafka_manager.start_consuming()

    def produce_message(self, topic, message):
        self.kafka_manager.send_message(f"{topic}.input", message.encode('utf-8'))

    def classify_input(self, message):
        decoded_message = message.value().decode('utf-8')
        self.classify_and_process(decoded_message)

    def classify_direct_input(self, message):
        self.classify_and_process(message)

    def classify_and_process(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        classified_message = {"message": message, "intent": output["labels"][0]}
        response = self.process_intent(message, output["labels"][0])

        # Send the classified message to the nlp_output topic
        self.kafka_manager.send_message(self.nlp_output_topic,
                                        {"classifier-agent": str(json.dumps(classified_message))})

    def process_intent(self, user_input, intent):
        # Hardcoded bot information
        bots_info = [
            {
                "name": "hotel-agent",
                "description": "This is an agent for hotel bookings.",
                "output_format": "json"
            },
            {
                "name": "restaurant-agent",
                "description": "This is an agent for restaurant recommendations.",
                "output_format": "json"
            },
            {
                "name": "city-guide-agent",
                "description": "This is an agent for most viewed places in a city.",
                "output_format": "json"
            },
            {
                "name": "festival-information-agent",
                "description": "Gives information about upcoming festivals.",
                "output_format": "json"
            },
            {
                "name": "google-search-agent",
                "description": "This is an agent for searching on Google.",
                "output_format": "json"
            },
            {
                "name": "flight-booking-agent",
                "description": "This is an agent for flight bookings.",
                "output_format": "json"
            }
        ]

        response = self.generate_response_with_langchain(user_input, bots_info)
        print(response)
        return response

    def generate_response_with_langchain(self, user_input, bots_info):
        context = " ".join([f"{bot['name']}: {bot['description']} ({bot['output_format']})" for bot in bots_info])

        prompt = PromptTemplate.from_template(
            """
            I want to answer the following question: {question}.
            How can I achieve this based on the following agents in my system: {context}.
            Give back only the names of all the agents that could be used to achieve this question.
            Do not explain anything, just give the names of the agents.
            """
        )

        chain = (
                RunnableParallel({
                    "context": str,
                    "question": RunnablePassthrough()
                })
                | prompt
                | self.model
                | StrOutputParser()
        )

        return chain.invoke({
            "context": context,
            "question": user_input
        })


if __name__ == "__main__":
    agent = ClassifierAgent(
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp.input",
        nlp_output_topic="nlp.output"
    )

    # Directly classify and process the input message
    agent.classify_direct_input("I want to travel to spain")
