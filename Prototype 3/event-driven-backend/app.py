from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pydantic import BaseModel, ValidationError
from kafka_client import KafkaClient
import json
import os
import logging

app = Flask(__name__)
api = Api(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get Kafka brokers from the environment variable
kafka_brokers = os.getenv('KAFKA_BROKERS', 'kafka:29092')
kafka_client = KafkaClient(kafka_brokers)


# Define a callback function to handle consumed messages
def process_message(key, value):
    app.logger.info(f"Consumed message: {key}, {value}")


# Start the Kafka consumer thread
kafka_client.start_consumer('events', process_message)


class Event(BaseModel):
    key: str
    value: dict


class ActivityPubEvent(BaseModel):
    context: str = "https://www.w3.org/ns/activitystreams"
    type: str
    actor: str
    object: dict


class ProduceEvent(Resource):
    def post(self):
        try:
            data = request.get_json()
            event = Event(**data)
            kafka_client.produce('events', event.key, json.dumps(event.value))
            return jsonify({"status": "success"})
        except ValidationError as e:
            app.logger.error(f"Validation error: {e}")
            return jsonify({"status": "error", "message": e.errors()})
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


class ProduceActivityPubEvent(Resource):
    def post(self):
        try:
            data = request.get_json()
            event = ActivityPubEvent(**data)
            kafka_client.produce('activitypub_events', event.actor, event.json())
            return jsonify({"status": "success"})
        except ValidationError as e:
            app.logger.error(f"Validation error: {e}")
            return jsonify({"status": "error", "message": e.errors()})
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


class ConsumeEvent(Resource):
    def get(self):
        try:
            events = []
            for key, value in kafka_client.consume('events'):
                events.append({"key": key.decode('utf-8'), "value": json.loads(value.decode('utf-8'))})
            return jsonify(events)
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


class ConsumeActivityPubEvent(Resource):
    def get(self):
        try:
            events = []
            for key, value in kafka_client.consume('activitypub_events'):
                events.append({"key": key.decode('utf-8'), "value": json.loads(value.decode('utf-8'))})
            return jsonify(events)
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


api.add_resource(ProduceEvent, '/produce')
api.add_resource(ProduceActivityPubEvent, '/activitypub')
api.add_resource(ConsumeEvent, '/consume')
api.add_resource(ConsumeActivityPubEvent, '/consume/activitypub')


@app.route('/')
def home():
    return "Kafka Event-Driven Service with Flask"


@app.teardown_appcontext
def shutdown_session(exception=None):
    kafka_client.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
