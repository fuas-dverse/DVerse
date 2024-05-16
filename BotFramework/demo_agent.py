from agent.agent import Agent
from kafka_manager import KafkaManager


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

    kafka = KafkaManager()

    kafka.send_message("hotel-agent.input", {"message": "Hello, World!"})
