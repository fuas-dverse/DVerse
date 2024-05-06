from pymilvus import connections, FieldSchema, CollectionSchema, DataType


def setup_milvus():
    # Connect to Milvus server
    connections.connect()

    # Create collection schema
    collection_name = 'my_collection'
    fields = [
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=768)
    ]
    collection_schema = CollectionSchema(fields=fields, description="My collection schema")

    # Create collection
    collection = connections.create_collection(collection_schema, collection_name=collection_name)

    # Create index on the 'embedding' field
    index_params = {'index_type': 'IVF_FLAT', 'params': {'nlist': 128}, 'metric_type': 'L2'}
    connections.create_index(collection, index_params=index_params)

    print("Milvus setup completed.")


if __name__ == "__main__":
    setup_milvus()
