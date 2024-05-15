from Agent import Agent

if __name__ == "__main__":
    agent = Agent(
        name="Demo Agent",
        description="This is a demo agent.",
        topics=["demo", "agent"],
        output_format="json"
    )

    agent.db_manager.similarity_search(["demo", "agent"])
