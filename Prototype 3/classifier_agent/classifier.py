import json
import requests
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from kafka_manager.kafka_manager import KafkaManager
from langchain_anthropic import ChatAnthropic


class ClassifierAgent:
    def __init__(self, classifier_model, nlp_input_topic, nlp_output_topic):
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)
        self.kafka_manager = KafkaManager()
        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.consume_messages(self.nlp_input_topic)

        # Initialize GPT-2 model and tokenizer
        # self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        # self.model = GPT2LMHeadModel.from_pretrained("gpt2")

        self.model = ChatAnthropic(model='claude-3-opus-20240229')

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
        print(response)

        # Send the classified message to the nlp_output topic
        self.kafka_manager.send_message(self.nlp_output_topic,
                                        {"classifier-agent": str(json.dumps(classified_message))})

    def process_intent(self, user_input, intent):
        bots_info = requests.get("http://localhost:8000/" + intent).json()

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
                "name": "cityGuide-agent",
                "description": "This is an agent for most viewed places in a city.",
                "output_format": "json"
            }
        ]
        print(bots_info)

        response = self.generate_response_with_langchain(user_input, bots_info)
        print(bots_info)
        return response

    def generate_response_with_langchain(self, user_input, bots_info):
        context = " ".join([f"{bot['name']}: {bot['description']} ({bot['output_format']})" for bot in bots_info])
        prompt = (f"Answer based on the following context: {context}. "
                  f"What steps need to be made in order to respond to: {user_input}?")

        # Generate response using the LangChain ChatAnthropic model
        response = self.model.run(prompt)
        return response.strip()


# if __name__ == "__main__":
#     agent = ClassifierAgent(
#         classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
#         nlp_input_topic="nlp.input",
#         nlp_output_topic="nlp.output"
#     )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Send a message to the ClassifierAgent')
    parser.add_argument('message', type=str, help='The message to classify and process')
    args = parser.parse_args()

    agent = ClassifierAgent(
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp.input",
        nlp_output_topic="nlp.output"
    )

    # Directly classify and process the input message
    agent.classify_direct_input(args.message)
