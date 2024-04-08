from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic


class MessageRouter:
    def __init__(self, server):
        self.producer = Producer({
            'bootstrap.servers': server
        })

        self.consumer = Consumer({
            'bootstrap.servers': server,
            'group.id': 'group',
            'auto.offset.reset': 'earliest'
        })

        self.admin = AdminClient({
            'bootstrap.servers': server
        })

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message.encode('utf-8'))
        self.producer.flush()

    def subscribe(self, topic, callback):
        if topic not in self._list_topics():
            self._create_topic(topic)

        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue
            callback(msg.value().decode('utf-8'))

    def _list_topics(self):
        return self.admin.list_topics().topics

    def _create_topic(self, topic, partitions=1, replication=1):
        new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
        fs = self.admin.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")

    def _delete_topic(self, topic):
        fs = self.admin.delete_topics([topic])
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} deleted")
            except Exception as e:
                print(f"Failed to delete topic {topic}: {e}")
