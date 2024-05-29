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
        self.model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", task="text-generation", temperature=0.8)
        self.kafka_manager = KafkaManager()
        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.consume_messages(self.nlp_input_topic)

    def consume_messages(self, topic):
        self.kafka_manager.subscribe(topic, self.classify_input)
        self.kafka_manager.start_consuming()

    def produce_message(self, topic, message):
        self.kafka_manager.send_message(f"{topic}.input", message.encode('utf-8'))

    def classify_input(self, message):
        decoded_message = message.value().decode('utf-8')
        self.classify_and_process(decoded_message)

    def classify_and_process(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        intent = output["labels"][0]
        response = self.process_intent(message, intent)
        json_message = {"classifier-agent": str(json.dumps({"message": message, "intent": intent, "steps": response}))}
        self.kafka_manager.send_message(self.nlp_output_topic, json_message)

    def process_intent(self, user_input, intent):
        bots_info = json.loads(requests.get(f"http://localhost:8000/{intent}").json()["message"])
        return self.extract_list_from_response(self.generate_response_with_langchain(user_input, bots_info))

    @staticmethod
    def extract_list_from_response(response):
        start_index = response.find('[') + 1
        end_index = response.find(']')
        list_string = response[start_index:end_index]
        list_string = list_string.replace("'", "")
        response_list = [item.strip() for item in list_string.split(',')]
        return response_list

    def generate_response_with_langchain(self, user_input, bots_info):
        context = " ".join([f"{bot['name']}: {bot['description']} ({bot['output_format']})" for bot in bots_info])

        prompt = PromptTemplate.from_template(
            """
            I want to answer the following question: {question}.
            How can I achieve this based on the following agents in my system: {context}.
            Give back all the agents that could be used to achieve this question.
            Do not explain anything, just give the the agents in the following array format: ['agent1', 'agent2', 'etc']
            Multiple agents are allowed!
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
            "question": user_input,
        })

    def send_to_agent(self, message, first_agent):
        self.produce_message(f"{first_agent}.input", message)


if __name__ == "__main__":
    agent = ClassifierAgent(
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp.input",
        nlp_output_topic="nlp.output"
    )
