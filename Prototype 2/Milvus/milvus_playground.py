#  _____                                                                                       _____ 
# ( ___ )                                                                                     ( ___ )
#  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
#  |   |  __  __ _ _                   _____  _                                             _  |   | 
#  |   | |  \/  (_) |                 |  __ \| |                                           | | |   | 
#  |   | | \  / |_| |_   ___   _ ___  | |__) | | __ _ _   _  __ _ _ __ ___  _   _ _ __   __| | |   | 
#  |   | | |\/| | | \ \ / / | | / __| |  ___/| |/ _` | | | |/ _` | '__/ _ \| | | | '_ \ / _` | |   | 
#  |   | | |  | | | |\ V /| |_| \__ \ | |    | | (_| | |_| | (_| | | | (_) | |_| | | | | (_| | |   | 
#  |   | |_|  |_|_|_| \_/  \__,_|___/ |_|    |_|\__,_|\__, |\__, |_|  \___/ \__,_|_| |_|\__,_| |   | 
#  |   |                                               __/ | __/ |                             |   | 
#  |   |                                              |___/ |___/                              |   | 
#  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
# (_____)                                                                                     (_____)

# This Python script is so you can test the Milvus functionalities
# Without starting the entire tree of bots
# 
# If this script is no longer necessary then please delete it
# Also because of this script I made a separate python script 
# with everything related to the Milvus functionalities (milvus_functions.py)

from milvus_functions import MilvusFunctions

milvus_instance = MilvusFunctions()

try:
    # Start the connection
    client = milvus_instance.enable_milvus_global()

    # Specify collection_name
    collection_name = "embeddings"

    # Ask a question
    question = "recommendations for hotels in Paris."

    # Embed the question
    embedded_question=milvus_instance.embed_text_dense(question)

    # Insert the question 
    ## Convert embeddings to Milvus-compatible format (FLOAT_VECTOR)
    embedding_vectors = [list(embedding) for embedding in embedded_question]

    data = [{"embedding_id": i, "embedding": embedding} for i, embedding in enumerate(embedding_vectors)]

    # print(data[0])
    
    dict_input= milvus_instance.input_embeddings(data=data,collection_name=collection_name)

    # Get entities
    ids = [0,1,2,3]
    entities= milvus_instance.get_entities(collection_name,id_list=ids)

    print("First entity: ",entities[0])

    # Search using similar/ follow-up  question 
    ## Ask a question
    question = "hotels in Rome."

    ## Embed the question
    embedded_question=milvus_instance.embed_text_dense(question)

    # Similar search
    output = milvus_instance.similarity_search(embedded_question,collection_name)

    print("Similar entities: ",output)

    # See all entities
    collection_result = milvus_instance.get_entities_collection(collection_name)
    print("Everything: ",collection_result)

finally:
    milvus_instance.close_milvus()
    print("Playground over")