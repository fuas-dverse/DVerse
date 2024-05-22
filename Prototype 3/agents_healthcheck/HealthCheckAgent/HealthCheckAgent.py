from confluent_kafka import Consumer, Producer
from DatabaseManager.DatabaseManager import DatabaseManager


class HealthCheckAgent:
    def __init__(self):
        self.databaseManager = DatabaseManager()
        self.agent = self.databaseManager.insert_data("HealthCheckAgent", "Health Check Agent", ["health", "check"],
                                                      "json", True)
        print("HealthCheckAgent initialized")

    def __get_all_agents(self):
        return self.databaseManager.get_all_data()
