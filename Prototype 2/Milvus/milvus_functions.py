from pymilvus import MilvusClient
from pymilvus import model

class MilvusFunctions:

    def __init__(self, host_url="http://localhost:19530"):
        self.client = MilvusClient(uri=host_url)
        self.host_url = host_url

    def enable_milvus_global(self):
        return self.client

    def enable_milvus_root(self):
        return MilvusClient(
            uri="http://localhost:19530",
            token="root:Milvus",
            db_name="default"
        )

    def enable_milvus_non_root(self, token="user:password"):
        return MilvusClient(
            uri="http://localhost:19530",
            token=token,
            db_name="default"
        )

    def close_milvus(self):
        return self.client.close()

    def embed_text_dense(self, query):
        sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
            model_name='distilbert-base-nli-mean-tokens',
            device='cpu'
        )
        query_embeddings = sentence_transformer_ef.encode_queries(query)
        return query_embeddings

    def input_embeddings(self, data: list, collection_name: str):
        return self.client.insert(collection_name, data=data)

    def similarity_search(self, query_vectors: list, collection_name: str):
        res = self.client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=3
        )
        return res

    def get_entities(self, collection_name: str, id_list: list, fields: list = None):
        return self.client.get(
            collection_name=collection_name,
            ids=id_list,
            output_fields=fields
        )

    def get_entities_collection(self, collection_name: str):
        return self.client.describe_collection(collection_name=collection_name)

    def remove_entities(self, collection_name: str, id_list: list):
        return self.client.delete(
            collection_name=collection_name,
            ids=id_list
        )
