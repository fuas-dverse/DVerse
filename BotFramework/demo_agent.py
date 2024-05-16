import time
from agent.agent import Agent


def callback(x):
    print(f"Message received {x.value().decode('utf-8')}")


if __name__ == "__main__":
    agent = Agent(
        name="Hotel Agent",
        description="This is a demo agent.",
        topics=["demo", "agent"],
        output_format="json",
        callback=callback
    )

    # Do some processing here
    time.sleep(2)

    agent.send_response_to_ui("Hello from the agent!")
