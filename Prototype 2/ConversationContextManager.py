from confluent_kafka import Producer
from transformers import pipeline
from pymilvus import MilvusClient, DataType, CollectionSchema, FieldSchema
from sentence-transformers import SentenceTransformer

class ConversationContextManager:
    def __init__(self, bootstrap_servers, message_topic, router):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
        self.message_topic = message_topic
        self.milvus_client = MilvusClient()  # Initialize Milvus client
        self.embedding_model = SentenceTransformer(
            'distilbert-base-nli-mean-tokens')  # Load pre-trained embedding model
        self.router = router

    def classify_and_route(self, message):
        output = self.classifier(message, ["language", "travel"], multi_label=False)
        classified_message = {"message": message, "intent": output["labels"][0]}
        # Store message embedding in Milvus
        embedding = self.calculate_embedding(message)
        self.store_embedding(embedding)
        self.router.route_message(output["labels"][0], self.message_topic, classified_message)
        return classified_message

    def calculate_embedding(self, message):
        # Calculate the embedding for the message using pre-trained model
        embedding = self.embedding_model.encode(message)  # Generate embedding using pre-trained model
        return embedding

    def store_embedding(self, embedding):
        # Store the embedding in Milvus
        collection_name = "message_embeddings"
        collection = self.milvus_client.get_collection_stats(collection_name)
        if not collection:
            # Create collection schema if it doesn't exist
            fields = [
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=len(embedding))
            ]
            collection_schema = CollectionSchema(fields=fields, description="Collection for storing message embeddings")
            collection = self.milvus_client.create_collection(collection_schema, collection_name=collection_name)
        self.milvus_client.insert(collection_name, [embedding])
