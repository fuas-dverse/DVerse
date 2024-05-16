import json
import flask
from flask import Response
from flask_socketio import SocketIO
from confluent_kafka import Producer, Consumer,KafkaError

# Create a Flask application
app = flask.Flask(__name__)

# Create a SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

# Create a Kafka producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Create a Kafka consumer
consumer = Consumer({'bootstrap.servers': 'localhost:9092','group.id': 'my-group','auto.offset.reset': 'earliest',})


def handle_output(message):
    """
    Handle the output from the agents to send back to UI over websocket connection.

    Parameters:
    message (str): The message to be sent back to the UI.
    """

    socketio.emit('message', {'data': json.loads(message.value().decode('utf-8'))})


@socketio.on('message')
def handle_message(message):
    """
    Handle incoming messages from chat screen UI to be sent to agents via Kafka.

    Parameters:
    message (str): The message sent by the user via UI chat interface.
    """
    producer.produce('classifier.input', value=message.encode('utf-8'))
    producer.flush()

@socketio.on('command')
def handle_command(topic:str,message):
    """
    Handle incoming commands from the UI interface that should be sent to   agents via Kafka.

    Parameters:
    topic   (str) : The Kafka topic where it needs to be send to.
    message (json): The Input of the command that is being send.
    """
    json_message= json.dumps(message)
    producer.produce(topic,value=json_message)
    producer.flush()

def events():
    print("Start events")
    result = []
    while True:
        msg = consumer.poll(5.0)
        if msg is None:
            print("Waiting...")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print("Result found")
        result.append(msg.value())
        print("Result appended")
        if len(result)>5:
            return result

@socketio.on('getContainer')
def send_container_data():
    print("Send container")
    consumer.subscribe(['DiD_containers'])
    results = events()    
    decoded_results = [result.decode("utf-8") for result in results]
    json_data = json.dumps(decoded_results)
    print("Results: ",json_data)
    socketio.emit('response_command',json_data)

def send_container_data():
    consumer.subscribe(['DiD_response'])
    return Response(events())

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
