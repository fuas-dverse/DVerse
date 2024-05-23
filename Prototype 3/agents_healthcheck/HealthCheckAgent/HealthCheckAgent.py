import logging

from confluent_kafka import Consumer, Producer
from DatabaseManager.DatabaseManager import DatabaseManager
from KafkaManager.KafkaManager import KafkaManager


class HealthCheckAgent:
    def __init__(self):
        self.databaseManager = DatabaseManager()
        # self.agent = self.databaseManager.insert_data("HealthCheckAgent", "Health Check Agent", ["health", "check"],
        #                                               "json", True)
        self.kafkaManager = KafkaManager()

    def consume_messages(self, topic):
        self.kafkaManager.subscribe(topic)
        self.kafkaManager.start_consuming()
