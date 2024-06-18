import json

from kafka_manager.kafka_manager import KafkaManager

if __name__ == "__main__":
    kafka_manager = KafkaManager()
    # message = {
    #     "@context": "https://www.w3.org/ns/activitystreams",
    #     "@type": "Object",
    #     "actor": "agent",
    #     "content": [
    #         {
    #             "type": "text",
    #             "value": "Response as array",
    #         },
    #         {
    #             "type": "text",
    #             "value": "Blah blah blah2",
    #         },
    #         {
    #             "type": "text",
    #             "value": "Blah blah blah4",
    #         },
    #     ],
    #     "chatId": "umtufgmv8gp70sdpps1d6d",
    # }

    message = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "@type": "Object",
        "actor": "agent",
        "content": [
            {
                "type": "text",
                "value": "Say hello to the world",
            },
            {
                "type": "img",
                "value": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2972&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            },
        ],
        "chatId": "zrkolrtyzgl4wuag6erlh",
    }
    message = json.dumps(message)
    kafka_manager.producer.produce("google-search.output", message)
    kafka_manager.producer.flush()
