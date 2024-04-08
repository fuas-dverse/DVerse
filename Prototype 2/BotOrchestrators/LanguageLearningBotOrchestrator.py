from confluent_kafka import Producer, Consumer
from ..LanguageLearningBots.GoogleBot import search_google
from ..LanguageLearningBots.YouTubeBot import search_youtube

class LanguageBotOrchestrator:
    def __init__(self, bootstrap_servers, group_id):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe(['language_input'])
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def process_message(self, message):
        print("Language Bot Orchestrator received message:", message)
        # Trigger GoogleBot and YouTubeBot and process responses
        google_results = search_google(message)
        google_response = "\n".join([f"Title: {item['title']}\nURL: {item['link']}" for item in google_results])
        youtube_results = search_youtube(message)
        youtube_response = "\n".join([f"Title: {item['snippet']['title']}\nURL: https://www.youtube.com/watch?v={item['id']['videoId']}" for item in youtube_results])
        self.send_message('language_output', google_response)
        self.send_message('language_output', youtube_response)

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()

# Example usage:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    language_bot_orchestrator = LanguageBotOrchestrator(bootstrap_servers, 'language_group')
