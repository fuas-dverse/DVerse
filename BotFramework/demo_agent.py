from agent.agent import Agent
from kafka_manager import KafkaManager


def callback(x):
    print(f"Message received {x.value().decode('utf-8')}")


if __name__ == "__main__":
    agent = Agent(
        name="Demo Agent",
        description="This is a demo agent.",
        topics=["demo", "agent"],
        output_format="json"
    )

    kafka = KafkaManager()

    kafka.subscribe("test", callback)
    kafka.start_consuming()

    kafka.send_message("test", {"message": "Hello, World!"})
