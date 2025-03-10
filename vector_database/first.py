from pymilvus import model
from pymilvus import MilvusClient, DataType, db, connections

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/matches/{query}")
def read_item(query: str):
    return performTask(query)

@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

# Run the server using: uvicorn filename:app --host 0.0.0.0 --port 8000 --reload

def performTask(query:str):
    
    pass

docs = [
  "He is diligent, reserved, loyal, impatient.",
  "She is adventurous, impulsive, empathetic, forgetful.",
  "He is cunning, charming, unforgiving, meticulous.",
  "She is optimistic, stubborn, creative, overthinking.",
  "He is easygoing, unmotivated, trusting, sarcastic.",
  "She is a perfectionist, reclusive, curious, judgmental.",
  "He is charismatic, reckless, protective, impatient.",
  "i am someone that is scared at nights, need someone to be with me at all the times."
]

sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2', 
    device='cpu' 
)

vectors  = sentence_transformer_ef.encode_documents(docs)
data = [ {"id": i, "vector": vectors[i], "text": docs[i]} for i in range(len(vectors)) ]

schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=True,
)

# Add fields to schema
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=384)
schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=512)


client = MilvusClient("./milvus_demo.db")
index_params = client.prepare_index_params()


#  Add indexes
index_params.add_index(
    field_name="vector", 
    index_type="AUTOINDEX",
    metric_type="COSINE"
)

# Create collection
client.create_collection(
    collection_name="demo_collection",
    schema=schema,
    index_params=index_params
)

# Insert data into collection
res = client.insert(
    collection_name="demo_collection",
    data=data
)

query = ["like to try new things and explore"]
query_embedding = sentence_transformer_ef.encode_queries(query)

# Load collection
client.load_collection(
    collection_name="demo_collection"
)

# Vector search
res = client.search(
    collection_name="demo_collection",
    data=query_embedding,
    limit=1,
    output_fields=["text"],
)
print(res)
"""
Output:
data: ["[{'id': 1, 'distance': 0.7199002504348755, 'entity': {'text': 'Alan Turing was the first person to conduct substantial research in AI.'}}]"] 
"""