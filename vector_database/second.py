from fastapi import FastAPI, HTTPException
from pymilvus import MilvusClient, DataType
from pymilvus import model
from fastapi import Body,Request

import uuid
import json

# 🚀 Initialize FastAPI App
app = FastAPI()

# 🌎 Global Milvus Client
client = MilvusClient("./milvus_demo.db")

# 📌 Initialize Sentence Transformer Embedding Model
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2', device='cpu'
)

# 📌 Define Collection Name
COLLECTION_NAME = "demo_collection"

# 📌 Create Collection Schema
def setup_milvus():
    schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=384)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=512)

    # Create Index Parameters
    index_params = client.prepare_index_params()
    index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")

    # Create Collection (if not exists)
    if not client.has_collection(COLLECTION_NAME):
        client.create_collection(collection_name=COLLECTION_NAME, schema=schema, index_params=index_params)
        print("✅ Milvus collection created successfully!")

    # Load Collection into Memory
    client.load_collection(collection_name=COLLECTION_NAME)

# 📌 Call setup function on startup
setup_milvus()

# 🔍 API: Get Similar Documents
@app.get("/matches/{query}")
def find_similar(query: str, limit: int = 3):
    query_embedding = sentence_transformer_ef.encode_queries([query])

    # Perform Vector Search
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        data=query_embedding,
        limit=limit,
        output_fields=["text"]
    )
    print(type(search_results))
    data = list(search_results)
    print(data[0][0])
    # search_results = search_results['data']
    # print(search_results)
    # search_results = json.load(search_results)
    # print(search_results)

    # Extract and Return Results
    matches = [{"id": hit["id"], "text": hit["entity"]["text"], "distance": hit["distance"]} for hit in data[0]]
    return {"query": query,"matches":matches}

# 🆕 API: Insert a New Document
@app.post("/items/")
def insert_item(text: str):
    vector = sentence_transformer_ef.encode_documents([text])[0]
    new_id = int(uuid.uuid4().int % (10**6))  # Generate Unique ID
    # Insert Data
    client.insert(
        collection_name=COLLECTION_NAME,
        data=[{"id": new_id, "vector": vector, "text": text}]
    )
    return {"message": "Item inserted successfully", "id": new_id, "text": text}

# 🔄 API: Upsert (Insert or Update)
@app.post("/upsert/")
# def upsert_item(id: int | None = None, text: str=Body()):
async def upsert_item(request: Request):
    data =await request.json()
    text=data['text']
    id=data['id']
    # print(text)
    vector = sentence_transformer_ef.encode_documents([text])[0]

    # Delete existing entry (if exists)
    client.delete(collection_name=COLLECTION_NAME, filter=f"id == {id}")

    # Insert updated entry
    client.insert(collection_name=COLLECTION_NAME, data=[{"id": id, "vector": vector, "text": text}])

    return {"message": "Upsert successful","id":id,"text":text}



# 🔄 API: Upsert (Insert or Update)
@app.post("/delete/")
# def upsert_item(id: int | None = None, text: str=Body()):
async def upsert_item(request: Request):
    data =await request.json()
    # text=data['text']
    id=data['id']
    # print(text)
    # vector = sentence_transformer_ef.encode_documents([text])[0]

    # Delete existing entry (if exists)
    client.delete(collection_name=COLLECTION_NAME, filter=f"id == {id}")

    # Insert updated entry
    # client.insert(collection_name=COLLECTION_NAME, data=[{"id": id, "vector": vector, "text": text}])

    return {"message": "delete successful","id":id}



# 🏠 API: Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Milvus-powered FastAPI is running!"}


@app.get("/all")
def read_all_rows():
    search_results=client.query(collection_name=COLLECTION_NAME,filter="id >= 0", output_fields=["id", "text"]);
    print(search_results)
    return search_results
# 🚀 Run the server using: uvicorn filename:app --host 0.0.0.0 --port 8000 --reload
