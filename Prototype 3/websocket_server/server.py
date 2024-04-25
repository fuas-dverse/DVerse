import json
import flask
from flask_socketio import SocketIO

app = flask.Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# Function to handle travel output messages
def handle_output(message):
    # Send message back to the UI
    socketio.emit('message', {'data': json.loads(message.value().decode('utf-8'))})


@socketio.on('message')
def handle_message(data):
    # Retrieve the conversation_manager from Flask's application context
    conversation_manager = flask.current_app.config['conversation_manager']

    # Send the user input to the ConversationContextManager for processing
    conversation_manager.classify_and_route(data)


if __name__ == "__main__":
    # Start the application
    socketio.run(app, port=5000, debug=True)
