from pymilvus import DataType, MilvusClient

def setup_milvus():
    #Connect to Milvus
    client = MilvusClient("http://localhost:19530")

    # Create the basic schema
    schema = client.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    # Add fields to schema
    schema.add_field(field_name="embedding_id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=768)

    # Prepare index parameters
    index_params = client.prepare_index_params()

    # Add indexes
    index_params.add_index(
        field_name="embedding_id"
    )

    index_params.add_index(
        field_name="embedding", 
        index_type="IVF_FLAT",
        metric_type="L2",
        params={'nlist': 128}
    )

    client.create_collection(
        collection_name="embeddings",
        schema=schema,
        index_params=index_params
    )

    print("Milvus setup completed.")
    client.close()

if __name__ == "__main__":
    setup_milvus()
