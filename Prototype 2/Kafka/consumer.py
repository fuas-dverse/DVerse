import threading
from time import sleep
from Kafka.MessageRouter import MessageRouter

message_router = MessageRouter("host.docker.internal:9092")


def callback(message):
    print(f"Received message: {message.value().decode('utf-8')}")

    # TODO: Add actual logic for handling the response (Process Agent Logic)
    # For now, just sleep for 5 seconds
    sleep(5)

    # Extract requestId Header from the message
    request_id = message.headers()[0][1].decode('utf-8')

    message_router.send_message("response", "{}".format("Request processed"), request_id)


def consume():
    message_router.subscribe("test", callback)


if __name__ == "__main__":
    threading.Thread(target=consume).start()
