from transformers import pipeline
from Kafka.MessageRouter import MessageRouter
from ConversationContextManager import ConversationContextManager
from BotOrchestrators.LanguageLearningBotOrchestrator import LanguageBotOrchestrator
from BotOrchestrators.TravelBotOrchestrator import TravelBotOrchestrator
import threading

# Function to handle language output messages
def handle_language_output(message):
    print("Language Output:", message.value().decode('utf-8'))

# Function to handle travel output messages
def handle_travel_output(message):
    print("Travel Output:", message.value().decode('utf-8'))

def main():
    # Initialize Kafka message router
    message_router = MessageRouter("host.docker.internal:9092")

    # Initialize ConversationContextManager
    conversation_manager = ConversationContextManager(
        bootstrap_servers="host.docker.internal:9092",
        message_topic="input_topic",
        router=message_router
    )

    # Initialize LanguageBotOrchestrator and TravelBotOrchestrator
    language_bot_orchestrator = LanguageBotOrchestrator("host.docker.internal:9092", "language_group")
    travel_bot_orchestrator = TravelBotOrchestrator("host.docker.internal:9092", "travel_group")

    user_input = input("Enter your message: ")
        # Send the user input to the ConversationContextManager for processing
    conversation_manager.classify_and_route(user_input)
    
    # Start consuming messages
    message_router.subscribe("input_topic", conversation_manager.classify_and_route)
    
    # Define a function to start consuming messages for a bot orchestrator
    def consume_messages(bot_orchestrator):
        bot_orchestrator.consume()

    # Start consuming messages for both bot orchestrators in separate threads
    language_thread = threading.Thread(target=consume_messages, args=(language_bot_orchestrator,))
    travel_thread = threading.Thread(target=consume_messages, args=(travel_bot_orchestrator,))
    
    language_thread.start()
    travel_thread.start()

    # Subscribe to output topics and handle output messages
    message_router.subscribe("language_output", handle_language_output)
    message_router.subscribe("travel_output", handle_travel_output)

    # Start consuming messages for all subscribed topics
    message_router.start_consuming()

    # Accept input from the user
    while True:
        user_input = input("Enter your message: ")
        # Send the user input to the ConversationContextManager for processing
        conversation_manager.classify_and_route(user_input)

if __name__ == "__main__":
    # Start the application
    main()
