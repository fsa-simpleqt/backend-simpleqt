import os
# from dotenv import load_dotenv

from app.modules.crud_question_test.models.crud_question_tests import get_question_test_by_id
from app.utils.text2vector import text2vector
from app.configs.database import firebase_bucket
from app.configs.qdrant_db import qdrant_client
    
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
    return question_test_url_list
