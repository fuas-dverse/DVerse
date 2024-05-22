from slugify import slugify
from database_manager.database_manager import DatabaseManager
from kafka_manager import KafkaManager
from status_manager import StatusManager


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

        self.__db_manager = DatabaseManager()
        self.__kafka_manager = KafkaManager()
        self.__status_manager = StatusManager(self.__kafka_manager, self.name)
        self.__initialize_bot()

    def __initialize_bot(self):
        """
        Initialize the bot, and insert bot data into database.
        """
        self.__db_manager.insert_data(self.name, self.description, self.topics, self.output_format, True)
        self.__kafka_manager.subscribe(f"{self.name}.input", self.callback)
        self.__kafka_manager.start_consuming()
        self.__status_manager.start_looping()

    def send_response_to_ui(self, message):
        """
        Send a response message to the UI.

        Args:
            message (dict[str, str]): The message to send to the UI.
        """
        self.__kafka_manager.send_message(f"{self.name}.output", {self.name: message})
