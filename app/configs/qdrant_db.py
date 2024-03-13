from qdrant_client import QdrantClient
from qdrant_client.http import models

import os
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url = os.getenv("QDRANT_URL"), 
    api_key = os.getenv("QDRANT_API_KEY"),
)
print("Qdrant Database connected")

# 2. Check if the question_tests exists
if qdrant_client.collection_exists('question_tests') == False:
    qdrant_client.create_collection(
    collection_name="question_tests",
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    print("Collection question_tests created")
# 3. Check if the rag_documents_test exists
elif qdrant_client.collection_exists('rag_documents_test') == False:
    qdrant_client.create_collection(
    collection_name="rag_documents_test",
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    print("Collection rag_documents_test created")
else:
    print("Collections already exist")
