import json
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint
from transformers import pipeline
from kafka_manager.kafka_manager import KafkaManager
import re


class ClassifierAgent:
    def __init__(self, classifier_model, nlp_input_topic, nlp_output_topic):
        self.classifier = pipeline("zero-shot-classification", model=classifier_model)
        self.model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", task="text-generation",
                                         temperature=0.8)
        self.kafka_manager = KafkaManager()
        self.nlp_input_topic = nlp_input_topic
        self.nlp_output_topic = nlp_output_topic
        self.consume_messages(self.nlp_input_topic)

    def consume_messages(self, topic):
        self.kafka_manager.subscribe(topic, self.classify_input)
        self.kafka_manager.start_consuming()

    # def produce_message(self, topic, message):
    #     self.kafka_manager.send_message(f"{topic}.input", message.encode('utf-8'))

    def classify_input(self, message):
        decoded_message = message.value().decode('utf-8')
        processed_message = self.check_and_convert(decoded_message)
        self.classify_and_process(processed_message)

    def classify_and_process(self, message):
        chat_id = message.get("chatId")
        message_content = message.get("content").get("value")
        topics = requests.get("http://34.91.141.27/get/topics").json()["message"]
        topics = json.loads(topics)

        if len(topics) == 0:
            return print("No topics available.")

        output = self.classifier(message_content, topics, multi_label=False)
        intent = output["labels"][0]

        try:
            response = self.process_intent(message_content, intent)
        except requests.exceptions.RequestException as e:
            print(f"Failed to process intent '{intent}': {e}")
            return e  # Return error message and keep polling for new messages

        json_message = self.check_and_convert(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "@type": "Object",
                "actor": "agent",
                "content": [
                    {
                        "agent": "classifier-agent",
                        "message": message_content,
                        "intent": intent,
                        "steps": response,
                    },
                ],
                "chatId": chat_id,
            }
        )

        # Convert dictionary to JSON string before sending
        json_message_str = json.dumps(json_message)

        self.kafka_manager.send_message(self.nlp_output_topic, json_message_str)
        self.kafka_manager.send_message(f"{response[0]}.input", json_message_str)

    def process_intent(self, user_input, intent):
        bots_info = json.loads(requests.get(f"http://34.91.141.27/{intent}").json()["message"])
        llm_response = self.generate_response_with_langchain(user_input, bots_info)

        if "1." in llm_response:
            return self.validate_and_convert_steps(llm_response)
        else:
            return self.extract_list_from_response(llm_response)

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
            Answer ONLY using the following agents: {context}
            I want to answer the following question: {question}.
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

    def check_and_convert(self, input_data):
        if isinstance(input_data, str):
            try:
                json_data = json.loads(input_data)
                return json_data
            except json.JSONDecodeError:
                raise ValueError("String is not a valid JSON")
        elif isinstance(input_data, dict):
            return input_data
        else:
            raise TypeError("Input must be a string or a JSON object")

    def validate_and_convert_steps(self, steps):
        return [part for part in steps.split() if part][1::2]


if __name__ == "__main__":
    agent = ClassifierAgent(
        classifier_model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        nlp_input_topic="nlp.input",
        nlp_output_topic="nlp.output"
    )

