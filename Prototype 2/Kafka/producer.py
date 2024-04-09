import uuid
import threading
from MessageRouter import MessageRouter


message_router = MessageRouter("host.docker.internal:9092", str(uuid.uuid4()))

current_request_id = None


def callback(message):
    request_id = message.headers()[0][1].decode('utf-8')

    if request_id == current_request_id:
        print(f"Received message: {message.value().decode('utf-8')}")


def consume():
    message_router.subscribe("response", callback)


def produce():
    global current_request_id
    current_request_id = str(uuid.uuid4())
    message_router.send_message("test", "Hello, World!", current_request_id)


if __name__ == "__main__":
    threading.Thread(target=consume).start()
    produce()
