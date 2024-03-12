from qdrant_client import QdrantClient
from qdrant_client.http import models

import os
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url = os.getenv("QDRANT_URL"), 
    api_key = os.getenv("QDRANT_API_KEY"),
)

try:
    collection_info = qdrant_client.get_collection("question_tests")
except Exception as e:
    qdrant_client.create_collection(
    collection_name="question_tests",
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
)
    
print("Qdrant Database connected")

