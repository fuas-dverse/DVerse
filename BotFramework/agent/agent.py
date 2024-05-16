from slugify import slugify
from database_manager.database_manager import DatabaseManager
from kafka_manager import KafkaManager


class Agent:
    def __init__(self, name, description, topics, output_format, callback=None):
        """
        Initialize an agent with specified attributes.

        Args:
            name (str): Name of the agent.
            description (str): Description of the agent.
            topics (list): List of topics the agent handles.
            output_format (str): Desired output format for the agent (e.g., "pdf", "link", "image").
            callback (func): Callback function to call when a message is received.
        """
        self.name = slugify(name)
        self.description = description
        self.topics = topics if isinstance(topics, list) else [topics]
        self.output_format = output_format
        self.callback = callback

        self.db_manager = DatabaseManager()
        self.kafka_manager = KafkaManager()
        self.initialize_bot()

    def initialize_bot(self):
        """
        Initialize the bot, and insert bot data into database.
        """
        self.db_manager.insert_data(self.name, self.description, self.topics, self.output_format)
        self.kafka_manager.subscribe(f"{self.name}.input", self.callback)
        self.kafka_manager.start_consuming()
