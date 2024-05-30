from kafka_manager.kafka_manager import KafkaManager

if __name__ == "__main__":
    kafka_manager = KafkaManager()
    kafka_manager.producer.produce("nlp.input",  "I want to travel to Paris")
    kafka_manager.producer.flush()
