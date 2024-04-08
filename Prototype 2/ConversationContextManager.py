from transformers import pipeline
from confluent_kafka import Producer, Consumer

class ConversationContextManager:
    def __init__(self, bootstrap_servers, group_id, input_topic, bot_orchestrators):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([input_topic])
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.bot_orchestrators = bot_orchestrators
        self.classifier = pipeline("zero-shot-classification")

    def process_message(self, message):
        print("Conversation Context Manager received message:", message)
        # Classify intent using pre-trained model
        intent, confidence = self.classify_intent(message)
        if confidence > 0.5:  # Consider intent only if confidence is above a threshold (need to check how this behaves)
            # Route message to the appropriate bot orchestrator
            if intent in self.bot_orchestrators:
                self.bot_orchestrators[intent].process_message(message)
            else:
                print(f"No bot orchestrator found for intent: {intent}")
        else:
            print("Intent not recognized with sufficient confidence")

    def classify_intent(self, message):
        # Classify intent using pre-trained model
        result = self.classifier(message, candidate_labels=["travel", "language"], multi_class=True)
        intent = result['labels'][0]
        confidence = result['scores'][0]
        return intent, confidence

# Example usage:
if __name__ == "__main__":
    from .BotOrchestrators.TravelBotOrchestrator import TravelBotOrchestrator
    from .BotOrchestrators.LanguageLearningBotOrchestrator import LanguageBotOrchestrator

    bootstrap_servers = 'localhost:9092'
    travel_bot_orchestrator = TravelBotOrchestrator(bootstrap_servers, 'travel_group')
    language_bot_orchestrator = LanguageBotOrchestrator(bootstrap_servers, 'language_group')

    bot_orchestrators = {
        "travel": travel_bot_orchestrator,
        "language": language_bot_orchestrator
    }

    conversation_context_manager = ConversationContextManager(bootstrap_servers, 'group_id', 'input_topic', bot_orchestrators)
