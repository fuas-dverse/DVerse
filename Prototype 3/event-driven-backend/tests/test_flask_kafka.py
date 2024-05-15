import requests

BASE_URL = "http://127.0.0.1:5000"


def simulate_user_input():
    url = f"{BASE_URL}/produce"
    payload = {
        "context": "https://www.w3.org/ns/activitystreams",
        "type": "Create",
        "actor": "https://example.com/users/1",
        "object": {
            "type": "Note",
            "content": "I would like to travel to Italy next summer."
        }
    }
    response = requests.post(url, json=payload)
    print(f"Produce User Input Event: {response.status_code}, {response.json()}")


if __name__ == "__main__":
    simulate_user_input()
