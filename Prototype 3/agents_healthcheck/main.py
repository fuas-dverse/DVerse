import functions_framework
import os
import threading
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException
from kafka_manager.KafkaManager import KafkaManager

load_dotenv()

# Dictionary to keep track of the agents and their last seen time
agent_last_seen = {}
# Time threshold in minutes
time_threshold_minutes = 5

# Initialize KafkaManager
kafka_manager = KafkaManager()


def agent_callback(msg):
    agent_id = msg.key().decode('utf-8')
    # Update the last seen time of the agent
    agent_last_seen[agent_id] = datetime.utcnow()


def check_agent_health():
    while True:
        current_time = datetime.utcnow()
        for agent_id, last_seen in list(agent_last_seen.items()):
            if current_time - last_seen > timedelta(minutes=time_threshold_minutes):
                # Mark agent as down
                print(f"Agent {agent_id} is down")
                # You can add code here to remove the agent from the database if needed
                del agent_last_seen[agent_id]
        time.sleep(60)  # Check every 60 seconds


# Subscribe to the Kafka topic and start consuming messages
kafka_topic = os.environ.get("KAFKA_TOPIC")
kafka_manager.subscribe(kafka_topic, agent_callback)
kafka_manager.start_consuming()

# Start agent health check thread
health_check_thread = threading.Thread(target=check_agent_health)
health_check_thread.start()


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
