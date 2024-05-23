import json
import re

from flask import Flask, jsonify
import os

from KafkaManager.KafkaManager import KafkaManager
from DatabaseManager.DatabaseManager import DatabaseManager

app = Flask(__name__)

databaseManager = DatabaseManager()


@app.route('/check')
def check():
    kafka_manager = KafkaManager()
    # agents = databaseManager.get_all_data()
    messages = kafka_manager.consume_messages('agents.status', 5)

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

    # messages = [
    #     "{'agent': 'google-search-agent', 'status': 'OK'}",
    #     "{'agent': 'hotel-agent', 'status': 'OK'}",
    #     "{'agent': 'language-agent', 'status': 'OK'}"
    # ]

    def convert_to_valid_json(message):
        return re.sub(r"\'", "\"", message)

    try:
        if not messages:
            return jsonify(["No messages received"])
        else:
            # Parse messages into a dictionary
            status_dict = {eval(convert_to_valid_json(msg))['agent']: eval(convert_to_valid_json(msg))['status'] for msg
                           in messages}

            # Update agents' is_active status
            for agent in agents:
                if agent['name'] in status_dict and status_dict[agent['name']] == 'OK':
                    agent['is_active'] = True
                else:
                    agent['is_active'] = False

            return jsonify(agents)
    except Exception as e:
        return jsonify(["Error occurred: " + str(e)])


if __name__ == "__main__":
    # kafkaManager = KafkaManager()
    #
    # agents = databaseManager.get_all_data()
    # messages = kafkaManager.consume_messages('agents.status', 10)
    #
    # print(messages)
    # print(agents)
    #
    # # Set to keep track of active agents
    # active_agents = set()
    #
    # for message in messages:
    #     message_data = json.load(message)
    #     if message_data.get('status') == 'OK':
    #         active_agents.add(message_data.get('agent_id'))
    #
    # # Update agents' is_active status based on received messages
    # for agent in agents:
    #     if agent['name'] not in active_agents:
    #         databaseManager.delete_agent(agent['pk'])  # First delete the agent from the database
    #         databaseManager.insert_data(agent['name'], agent['description'], agent['topics'], agent['output_format'],
    #                                     False)  # Then re-insert the agent with is_active=False

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
