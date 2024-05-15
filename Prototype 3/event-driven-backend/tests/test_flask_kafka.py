import os
import requests
from dotenv import load_dotenv

load_dotenv()


class KafkaTester:
    def __init__(self, base_url):
        self.base_url = base_url

    def simulate_user_input(self, user_input):
        url = f"{self.base_url}/produce"
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
    tester = KafkaTester(os.getenv('BASE_URL'))
    user_input = input("Enter a question: ")
    tester.simulate_user_input(user_input)
