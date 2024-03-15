import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.evaluation import load_evaluator
from langchain.evaluation import EmbeddingDistance

from app.modules.crud_question_test.models.crud_question_tests import get_question_test_by_id
from app.modules.question_tests_retrieval.models.text2vector import text2vector
from app.configs.database import firebase_bucket
from app.configs.qdrant_db import qdrant_client

# Import API key
load_dotenv()

# Define the google api key
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Setting model embedding
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY, request_timeout=120)
gemini_evaluator = load_evaluator("embedding_distance", distance_metric=EmbeddingDistance.COSINE, embeddings=embedding_model)
    
def compare_vector(description_vector, max_number_of_points=1):
    similarity_list = qdrant_client.search(
        collection_name="question_tests",
        query_vector=description_vector,
        limit=max_number_of_points,
        with_vectors=False,
        with_payload=True,
    )

    formatted_similarity_list = []
    for point in similarity_list:
        formatted_similarity_list.append({"id": point.payload.get("id"), "score": point.score})

    return formatted_similarity_list

def download_question_test(question_test_url_list: list):
    # check folder exist
    if not os.path.exists('data/question_tests'):
        os.makedirs('data/question_tests')
    # download file from firebase storage using "gs://" link
    for url in question_test_url_list:
        name_bucket = url.split(f"gs://{firebase_bucket.name}/")[1]
        blob = firebase_bucket.blob(name_bucket)
        blob.download_to_filename(f'data/question_tests/{name_bucket}')
    return True

def get_question_tests(text: str):
    # Get formatted similarity list
    formatted_similarity_list = compare_vector(text2vector(text))
    # Get corresponding document url in Firebase and download them
    question_test_url_list = []
    for point in formatted_similarity_list:
        id = point.get("id")
        question_tests_url = get_question_test_by_id(id).get("question_tests_url")
        match_score = point.get("score")
        question_test_url_list.append({"id": id, "question_tests_url": question_tests_url, "match_score": match_score})

    # if download_question_test(question_test_url_list):
    #     return True
    # else:
    #     return False
    
    return question_test_url_list
