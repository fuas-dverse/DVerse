import threading

from Kafka.MessageRouter import MessageRouter

message_router = MessageRouter("host.docker.internal:9092")


def callback(message):
    print(f"Received message: {message}")

    # TODO: Add actual logic for handling the response (Process Agent Logic)

    message_router.send_message("response", "{}".format(message))


def consume():
    message_router.subscribe("test", callback)


if __name__ == "__main__":
    threading.Thread(target=consume).start()
