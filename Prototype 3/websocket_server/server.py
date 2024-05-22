import flask
from flask_socketio import SocketIO
from kafka_manager import KafkaManager

# Create a Flask application
app = flask.Flask(__name__)

# Create a SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

kafka_manager = KafkaManager()


def handle_output(message):
    """
    Handle the output from the agents to send back to UI over websocket connection.

    Parameters:
    message (str): The message to be sent back to the UI.
    """

    print(message.value().decode('utf-8'))

    # socketio.emit('message', {'data': json.loads(message.value().decode('utf-8'))})


@socketio.on('message')
def handle_message(message):
    """
    Handle incoming messages from chat screen UI to be sent to agents via Kafka.

    Parameters:
    message (str): The message sent by the user via UI chat interface.
    """

    print(message)

    kafka_manager.send_message("nlp.input", message)


if __name__ == "__main__":
    kafka_manager.subscribe(r"^.*\.output$", handle_output)
    kafka_manager.start_consuming()

    socketio.run(app, port=19256, debug=True)
