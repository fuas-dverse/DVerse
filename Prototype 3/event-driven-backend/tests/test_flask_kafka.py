import os

import requests
from dotenv import load_dotenv

load_dotenv()


def simulate_user_input(user_input):
    url = f"{os.getenv('BASE_URL')}/produce"
    payload = {
        "context": "https://www.w3.org/ns/activitystreams",
        "type": "Create",
        "actor": "https://example.com/users/1",
        "object": {
            "type": "Note",
            "content": user_input
        }
    }
    response = requests.post(url, json=payload)
    print(f"Produce User Input Event: {response.status_code}, {response.json()}")


if __name__ == "__main__":
    user_input = input("Enter a question: ")
    simulate_user_input(user_input)
