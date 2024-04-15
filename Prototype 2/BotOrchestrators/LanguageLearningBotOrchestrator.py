from BotOrchestrators.BotOrchestrator import BotOrchestrator
from LanguageLearningBots import search_google, search_youtube


class LanguageBotOrchestrator(BotOrchestrator):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            bot_type='LanguageBot',
            input_topic='language_input',
            output_topic='topic_output',
            search_function=self.search_language
        )

    def search_language(self, message):
        google_results = search_google(message)
        youtube_results = search_youtube(message)
        return google_results, youtube_results

    def consume(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            self.process_message(msg.value().decode('utf-8'))

    def format_response(self, search_results):
        google_results, youtube_results = search_results
        google_response = "\n".join([f"Title: {item['title']}\nURL: {item['link']}" for item in google_results])
        youtube_response = "\n".join(
            [f"Title: {item['snippet']['title']}\nURL: https://www.youtube.com/watch?v={item['id']['videoId']}" for item
             in youtube_results])
        return google_response + "\n" + youtube_response


# Example:
if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    language_bot_orchestrator = LanguageBotOrchestrator(bootstrap_servers, 'language_group')
