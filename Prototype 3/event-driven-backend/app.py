from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pydantic import BaseModel, ValidationError
from kafka_client import KafkaClient
import os
import logging


class Config:
    KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'kafka:29092')


class Event(BaseModel):
    context: str = "https://www.w3.org/ns/activitystreams"
    type: str
    actor: str
    object: dict


class ProduceEvent(Resource):
    def __init__(self, kafka_client):
        self.kafka_client = kafka_client

    def post(self):
        try:
            data = request.get_json()
            event = Event(**data)
            event_type = event.type.lower()
            object_type = event.object['type'].lower()
            topic = f"{event_type}_{object_type}"
            self.kafka_client.produce(topic, event.actor, event.json())
            return jsonify({"status": "success"})
        except ValidationError as e:
            app.logger.error(f"Validation error: {e}")
            return jsonify({"status": "error", "message": e.errors()})
        except Exception as e:
            app.logger.error(f"Exception: {e}")
            return jsonify({"status": "error", "message": str(e)})


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    kafka_client = KafkaClient(Config.KAFKA_BROKERS)

    api.add_resource(ProduceEvent, '/produce', resource_class_args=(kafka_client,))

    @app.route('/')
    def home():
        return "Kafka Event-Driven Service with Flask"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        kafka_client.close()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
