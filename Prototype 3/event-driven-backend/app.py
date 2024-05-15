from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pydantic import BaseModel, ValidationError
from kafka_client import KafkaClient
from confluent_kafka.admin import AdminClient, NewTopic

import os
import logging

app = Flask(__name__)
api = Api(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get Kafka brokers from the environment variable
kafka_brokers = os.getenv('KAFKA_BROKERS', 'kafka:29092')
kafka_client = KafkaClient(kafka_brokers)
topics = ['create_note', 'create_object']


def create_kafka_topics(topics):
    admin_client = AdminClient({'bootstrap.servers': 'host.docker.internal:9092'})

    topic_list = []
    for topic in topics:
        topic_list.append(NewTopic(topic, num_partitions=1, replication_factor=1))

    # Create topics
    fs = admin_client.create_topics(topic_list)

    # Wait for each operation to finish
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")


# Create topics
create_kafka_topics(topics)


# Define a callback function to handle consumed messages
def process_message(key, value):
    app.logger.info(f"Consumed message: {key}, {value}")


class Event(BaseModel):
    context: str = "https://www.w3.org/ns/activitystreams"
    type: str
    actor: str
    object: dict


class ProduceEvent(Resource):
    def post(self):
        try:
            data = request.get_json()
            event = Event(**data)
            event_type = event.type.lower()
            object_type = event.object['type'].lower()
            topic = f"{event_type}_{object_type}"
            kafka_client.produce(topic, event.actor, event.json())
            return jsonify({"status": "success"})
        except ValidationError as e:
            app.logger.error(f"Validation error: {e}")
            return jsonify({"status": "error", "message": e.errors()})
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


api.add_resource(ProduceEvent, '/produce')


@app.route('/')
def home():
    return "Kafka Event-Driven Service with Flask"


@app.teardown_appcontext
def shutdown_session(exception=None):
    kafka_client.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
