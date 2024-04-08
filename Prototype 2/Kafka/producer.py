from MessageRouter import MessageRouter
import threading

message_router = MessageRouter("host.docker.internal:9092")


def callback(message):
    print(f"Received message: {message}")


def consume():
    message_router.subscribe("response", callback)


if __name__ == "__main__":
    threading.Thread(target=consume).start()
    message_router.send_message("test", "Hello, World!")
