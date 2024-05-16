import os
from dotenv import load_dotenv
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.collection_name = "agents"
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.init_milvus()

    def init_milvus(self):
        connections.connect("default", uri=os.environ.get("MILVUS_URI"), token=os.environ.get("MILVUS_TOKEN"))
        if not self.check_collection():
            self.create_collection()

    def check_collection(self):
        return utility.has_collection(self.collection_name)

    def create_collection(self):
        fields = [
            FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
            FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="topics", dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=100, max_length=100),
            FieldSchema(name="output_format", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=384)
        ]
        schema = CollectionSchema(fields, "Database collection where context of agents will be stored.")
        Collection(self.collection_name, schema)

    def insert_data(self, name, description, topics, output_format):
        embeddings = self.generate_embeddings(topics)
        entities = [
            [name],
            [description],
            [topics],
            [output_format],
            [embeddings]
        ]

        collection = Collection(self.collection_name)
        collection.insert(entities)
        collection.load()

    def generate_embeddings(self, topics):
        return  self.embedding_model.encode(" ".join(topics)).tolist()

    def get_relevant_bots(self, query):
        collection = Collection(self.collection_name)
        query_embedding = self.generate_embeddings([query])
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        result = collection.search(
            data=[query_embedding],
            anns_field="embeddings",
            param=search_params,
            limit=3,
            expr=None,
            output_fields=["name", "description", "output_format"]
        )
        bots_info = []
        for res in result[0]:
            bots_info.append({
                "name": res.entity.get("name"),
                "description": res.entity.get("description"),
                "output_format": res.entity.get("output_format")
            })
        return bots_info
