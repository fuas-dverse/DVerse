import json
import flask
import requests
from flask import request
from flask_socketio import SocketIO
from kafka_manager import KafkaManager

# Create a Flask application
app = flask.Flask(__name__)

# Create a SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

kafka_output_manager = KafkaManager()
kafka_container_manager = KafkaManager()


@app.route('/emit', methods=['POST'])
def emit():
    """
    Emit a message to the UI via the websocket connection.
    """
    message = request.get_json()
    print(message)

    chat_id = message.get('chatId')

    socketio.emit(f"response-{chat_id}", message)
    return "Message emitted!"


def handle_output(message):
    """
    Handle the output from the agents to send back to UI over websocket connection.

    Parameters:
    message (str): The message to be sent back to the UI.
    """
    message_dict = json.loads(message)
    chat_id = message_dict.get('chatid')

    print(chat_id)
    print(f"sending to message: response-{chat_id}")
    response = requests.post('http://34.32.230.74/emit', json=message_dict)


@socketio.on('message')
def handle_message(message):
    """
    Handle incoming messages from chat screen UI to be sent to classifier via Kafka.

    Parameters:
    message (str): The message sent by the user via UI chat interface.
    """
    chat_id = message.get('chatId')
    socketio.emit(f"response-{chat_id}", message)

    kafka_output_manager.send_message('nlp.input', message)


@socketio.on('createChat')
def handle_created_chat(message):
    """
    Handle incoming chat creation from the UI interface to be sent to agents via Kafka.

    Parameters:
    message (str): The chat message sent by the user via UI chat interface.
    """
    socketio.emit("refreshChats", message)


@socketio.on('deleteChat')
def handle_delete_chat(message):
    """
    Handle incoming chat deletion from the UI interface to be sent to agents via Kafka.
    """
    socketio.emit("refreshChats", message)


@socketio.on('command')
def handle_command(topic: str, message):
    """
    Handle incoming commands from the UI interface that should be sent to   agents via Kafka.

    Parameters:
    topic   (str) : The Kafka topic where it needs to be sent to.
    message (json): The Input of the command that is being sent.
    """
    json_message = json.dumps(message)
    kafka_container_manager.send_message(topic, message=json_message)


def retrieve_data_kafka(message):
    result = message.value().decode('utf-8')
    socketio.emit("response_DiD", result)


def send_container_data(message):
    print("normal:" + message)
    socketio.emit('response_command', message)


@socketio.on('getResponse')
def retrieve_container_data():
    kafka_container_manager.subscribe("DiD_response", retrieve_data_kafka)
    kafka_container_manager.start_consuming()


@app.route('/', methods=['GET'])
def index():
    return "This is the DVerse Websocket Server"


if __name__ == "__main__":
    kafka_output_manager.subscribe(r"^.*\.output$", handle_output)
    kafka_output_manager.start_consuming()

    kafka_container_manager.subscribe("DiD_containers", send_container_data)
    kafka_container_manager.start_consuming()

    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, use_reloader=False, log_output=True,
                 cors_allowed_origins="*", port=80)
