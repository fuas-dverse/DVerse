from DatabaseManager.DatabaseManager import DatabaseManager
from KafkaManager.KafkaManager import KafkaManager
import time

databaseManager = DatabaseManager()
kafkaManager = KafkaManager()

if __name__ == "__main__":
    index = 1
    # databaseManager.insert_data("google-search-agent", "This searches the internet", ["test", "test"], "json", True)
    # databaseManager.insert_data("hotel-agent", "This helps you book an hotel", ["test", "test"], "json", True)
    # databaseManager.insert_data("language-agent", "Helps you with learning a language", ["test", "test"], "json", True)
    while True:
        kafkaManager.send_message("agents.status", {"agent": f"google-search-agent", "status": "OK"})
        kafkaManager.send_message("agents.status", {"agent": f"hotel-agent", "status": "OK"})
        kafkaManager.send_message("agents.status", {"agent": f"language-agent", "status": "OK"})
        # Index is just for testing if i got the last messages that i keep track of with the index
        index += 1
        time.sleep(5)
