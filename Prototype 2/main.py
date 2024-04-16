import json
import threading
import flask
from flask_socketio import SocketIO
from BotOrchestrators.LanguageLearningBotOrchestrator import LanguageBotOrchestrator
from BotOrchestrators.TravelBotOrchestrator import TravelBotOrchestrator
from ConversationContextManager import ConversationContextManager
from Kafka.MessageRouter import MessageRouter

app = flask.Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


# Function to handle travel output messages
def handle_output(message):
    # Send message back to the UI
    socketio.emit('message', {'data': json.loads(message.value().decode('utf-8'))})


def main():
    # Initialize Kafka message router
    message_router = MessageRouter("host.docker.internal:9092")

    # Initialize ConversationContextManager
    conversation_manager = ConversationContextManager(
        bootstrap_servers="host.docker.internal:9092",
        message_topic="input_topic",
        router=message_router
    )

    # Store conversation_manager in Flask's application context
    app.config['conversation_manager'] = conversation_manager

    # Initialize LanguageBotOrchestrator and TravelBotOrchestrator
    language_bot_orchestrator = LanguageBotOrchestrator("host.docker.internal:9092", "language_group")
    travel_bot_orchestrator = TravelBotOrchestrator("host.docker.internal:9092", "travel_group")

    # Define a function to start consuming messages for a bot orchestrator
    def consume_messages(bot_orchestrator):
        bot_orchestrator.consume()

    # Start consuming messages for both bot orchestrators in separate threads
    language_thread = threading.Thread(target=consume_messages, args=(language_bot_orchestrator,))
    travel_thread = threading.Thread(target=consume_messages, args=(travel_bot_orchestrator,))

    language_thread.start()
    travel_thread.start()

    # Subscribe to output topics and handle output messages
    message_router.subscribe("topic_output", handle_output)

    # Start consuming messages for all subscribed topics
    message_router.start_consuming()


@socketio.on('message')
def handle_message(data):
    # Retrieve the conversation_manager from Flask's application context
    conversation_manager = flask.current_app.config['conversation_manager']

    # Send the user input to the ConversationContextManager for processing
    conversation_manager.classify_and_route(data)


if __name__ == "__main__":
    # Start the application
    main()
    socketio.run(app, port=5000, debug=True)
