from flask import Flask, jsonify
import os
from KafkaManager.KafkaManager import KafkaManager
from DatabaseManager.DatabaseManager import DatabaseManager
from HealthCheckAgent.HealthCheckAgent import HealthCheckAgent

app = Flask(__name__)

kafkaManager = KafkaManager()
databaseManager = DatabaseManager()

@app.route('/')
def hello():
    return "Hello, World!"


@app.route('/check')
def check():
    topic = 'agents.status'
    messages = kafkaManager.get_all_messages_from_last_5_minutes(topic)
    return messages


if __name__ == "__main__":
    # healthCheckAgent = HealthCheckAgent()
    databaseManager.delete_agent("449908117299320524")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
