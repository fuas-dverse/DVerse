import requests
import json

BASE_URL = "http://127.0.0.1:5000"


def test_produce_event():
    url = f"{BASE_URL}/produce"
    payload = {
        "key": "testKey",
        "value": {"message": "Hello, Kafka!"}
    }
    response = requests.post(url, json=payload)
    print(f"Produce Event: {response.status_code}, {response.json()}")


def test_produce_activitypub_event():
    url = f"{BASE_URL}/activitypub"
    payload = {
        "context": "https://www.w3.org/ns/activitystreams",
        "type": "Create",
        "actor": "https://example.com/users/1",
        "object": {
            "type": "Note",
            "content": "Hello, world!"
        }
    }
    response = requests.post(url, json=payload)
    print(f"Produce ActivityPub Event: {response.status_code}, {response.json()}")


def test_consume_event():
    url = f"{BASE_URL}/consume"
    response = requests.get(url)
    print(f"Consume Event: {response.status_code}, {response.json()}")


def test_consume_activitypub_event():
    url = f"{BASE_URL}/consume/activitypub"
    response = requests.get(url)
    print(f"Consume ActivityPub Event: {response.status_code}, {response.json()}")


if __name__ == "__main__":
    test_produce_event()
    test_produce_activitypub_event()
    test_consume_event()
    test_consume_activitypub_event()
