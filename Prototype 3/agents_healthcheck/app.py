import os
import re
from flask import Flask, jsonify
from KafkaManager.KafkaConsumer import KafkaConsumerThread, message_cache
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/check')
def check():
    agents = [
        {'name': 'test - 3', 'description': 'Test Agent', 'topics': ['test', 'test'], 'output_format': 'json',
         'is_active': True, 'pk': '449908117299321143'},
        {'name': 'test - 2', 'description': 'Test Agent', 'topics': ['test', 'test'], 'output_format': 'json',
         'is_active': True, 'pk': '449908117299321143'},
        {'name': 'test - 1', 'description': 'Test Agent', 'topics': ['test', 'test'], 'output_format': 'json',
         'is_active': True, 'pk': '449908117299321146'},
        {'name': 'google-search-agent', 'description': 'This searches the internet', 'topics': ['test', 'test'],
         'output_format': 'json', 'is_active': True, 'pk': '449908117299321148'},
        {'name': 'hotel-agent', 'description': 'This helps you book an hotel', 'topics': ['test', 'test'],
         'output_format': 'json', 'is_active': True, 'pk': '449908117299321150'},
        {'name': 'language-agent', 'description': 'Helps you with learning a language', 'topics': ['test', 'test'],
         'output_format': 'json', 'is_active': True, 'pk': '449908117299321152'}
    ]

    def convert_to_valid_json(message):
        return re.sub(r"\'", "\"", message)

    try:
        messages = []
        while not message_cache.empty():
            messages.append(message_cache.get())

        if not messages:
            return jsonify(["No messages received"])
        else:
            status_dict = {eval(convert_to_valid_json(msg))['agent']: eval(convert_to_valid_json(msg))['status'] for msg
                           in messages}

            for agent in agents:
                if agent['name'] in status_dict and status_dict[agent['name']] == 'OK':
                    agent['is_active'] = True
                else:
                    agent['is_active'] = False

            return jsonify(agents)
    except Exception as e:
        return jsonify(["Error occurred: " + str(e)])


if __name__ == "__main__":
    # Start the Kafka consumer thread
    kafka_consumer_thread = KafkaConsumerThread()
    kafka_consumer_thread.start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    kafka_consumer_thread.stop()
