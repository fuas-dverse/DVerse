import json
import flask
from flask_socketio import SocketIO
from confluent_kafka import Producer

# Create a Flask application
app = flask.Flask(__name__)

# Create a SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

# Create a Kafka producer
producer = Producer({'bootstrap.servers': 'host.docker.internal:9092'})


def handle_output(message):
    """
    Handle the output from the agents to send back to UI over websocket connection.

    Parameters:
    message (str): The message to be sent back to the UI.
    """

    socketio.emit('message', {'data': json.loads(message.value().decode('utf-8'))})


@socketio.on('message')
def handle_message(message):
    """
    Handle incoming messages from chat screen UI to be sent to agents via Kafka.

    Parameters:
    message (str): The message sent by the user via UI chat interface.
    """
    producer.produce('classifier.input', value=message.encode('utf-8'))
    producer.flush()


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)