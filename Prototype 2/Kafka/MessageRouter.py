import threading
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from langchain import LangChain

from DatabaseManager import DatabaseManager


class MessageRouter:
    def __init__(self, server, group_id="default"):
        self.producer = Producer({'bootstrap.servers': server})
        self.consumer = Consumer({'bootstrap.servers': server, 'group.id': group_id, 'auto.offset.reset': 'earliest'})
        self.admin = AdminClient({'bootstrap.servers': server})
        self.subscriptions = {}
        self.db_manager = DatabaseManager()
        self.llm = LangChain(model="gpt-3.5-turbo")

    def route_message(self, label, topic, message):
        headers = {'requestId': None}
        if label == "language":
            self.send_message('language_input', message)
        elif label == "travel":
            self.send_message('travel_input', message)

    def send_message(self, topic, message, key=None):
        headers = {'requestId': key}
        if isinstance(message, dict):  # Check if message is a dictionary
            message = str(message)  # Convert dictionary to string
        self.producer.produce(topic, value=message.encode('utf-8'), headers=headers)
        self.producer.flush()

    def start_consuming(self):
        # Start consuming messages
        for topic, callback in self.subscriptions.items():
            threading.Thread(target=self._consume_messages, args=(topic, callback)).start()

    def subscribe(self, topic, callback):
        if topic not in self._list_topics():
            self._create_topic(topic)

        # Add the callback to the subscriptions dictionary
        self.subscriptions[topic] = callback

    def _list_topics(self):
        return self.admin.list_topics().topics

    def _create_topic(self, topic, partitions=1, replication=1):
        new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
        fs = self.admin.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    def _delete_topic(self, topic):
        fs = self.admin.delete_topics([topic])
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} deleted")
            except Exception as e:
                print(f"Failed to delete topic {topic}: {e}")

    def _consume_messages(self, topic, callback):
        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            callback(msg)

    def process_intent(self, user_input, intent):
        bots_info = self.db_manager.get_relevant_bots(intent)
        response = self.generate_response_with_langchain(user_input, bots_info)
        return response

    def generate_response_with_langchain(self, user_input, bots_info):
        context = " ".join([f"{bot['name']}: {bot['description']} ({bot['output_format']})" for bot in bots_info])
        prompt = f"Answer based on the following context: {context}. What steps need to be made in order to respond to: {user_input}?"

        response = self.llm(prompt)
        return response