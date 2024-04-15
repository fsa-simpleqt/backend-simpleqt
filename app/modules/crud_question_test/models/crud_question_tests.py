import uuid
import os
import json
from urllib.request import urlopen
from app.configs.database import firebase_bucket, firebase_db
from app.configs.qdrant_db import qdrant_client, models
from app.utils.text2vector import text2vector

from datetime import datetime
import pytz

# CRUD operation
def upload_file_question_tests(file_path):
    # upload file to firebase storage from file_path
    name_file = file_path.split("/")[-1]
    # upload file to folder "question_tests" in firebase storage
    blob = firebase_bucket.blob(f"question_tests/{name_file}")
    blob.upload_from_filename(file_path)
    blob.make_public()
    # return Download URL of the file
    return blob.public_url

def remove_file_question_tests(question_tests_file_name):
    # remove file from firebase storage question_tests_file_name
    blob = firebase_bucket.blob("question_tests/" + question_tests_file_name)
    blob.delete()
    return True

def get_all_question_tests():
    # Get all documents from the collection
    docs = firebase_db.collection("question_tests").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_question_tests"] = doc.id
        data.append(doc_data)
    return data

def get_question_test_by_id(id_question_tests):
    # Get a document by id
    doc = firebase_db.collection("question_tests").document(id_question_tests).get()
    # add id_question_tests to doc_data
    doc_data = doc.to_dict()
    doc_data["id_question_tests"] = doc.id
    return doc_data

def get_question_test_url_by_description(description):
    # Get a question_tests_url where question_tests_description is equal to description
    docs = firebase_db.collection("question_tests").where("question_tests_description", "==", description).stream()
    for doc in docs:
        return doc.to_dict()["question_tests_url"]
    return False

def get_question_test_data_by_id(id_question_tests: str):
    # Get a document by id
    doc = firebase_db.collection("question_tests").document(id_question_tests).get()
    doc = doc.to_dict()
    doc["id_question_tests"] = id_question_tests
    # store the response of URL 
    response = urlopen(doc["question_tests_url"])
    data_question_tests_json = json.loads(response.read())
    doc["exam_data"] = data_question_tests_json
    return doc


def create_question_test(data):
    # get file_question_tests
    file_question_tests = data["file_question_tests"]
    # rename file name to uuid
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file_question_tests.filename
    # save uploaded file to tmp folder
    cache_path = f"tmp/{re_name_file}"
    with open(cache_path, "wb") as buffer:
        buffer.write(file_question_tests.file.read())

    # upload file to firebase storage
    public_url_link = upload_file_question_tests(cache_path)
    # delete file in tmp folder
    os.remove(cache_path)

    # Get the current time in UTC
    utc_now = datetime.now()
    # Specify the Vietnam time zone
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    # Convert the current time to Vietnam time zone
    vietnam_now = utc_now.replace(tzinfo=pytz.utc).astimezone(vietnam_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    # create a new document
    firebase_save_data = {}
    # add vietnam_now to firebase_save_data
    firebase_save_data["created_at"] = vietnam_now
    # add question_tests_url to firebase_save_data
    firebase_save_data["question_tests_url"] = public_url_link
    # add file_name to firebase_save_data
    firebase_save_data["question_tests_file_name"] = re_name_file
    # add question_tests_description to firebase_save_data
    firebase_save_data["question_tests_description"] = data["question_tests_description"]
    
    # Create a new document
    document_ref = firebase_db.collection("question_tests").add(firebase_save_data)
    document_id = document_ref[1].id

    # Upload vector to Qdrant
    question_tests_des = data["question_tests_description"]
    collection_info = qdrant_client.get_collection('question_tests')
    points_count = collection_info.points_count
    description_vector = text2vector(question_tests_des)
    payload = {"id": document_id}
    point = models.PointStruct(id=points_count+1, payload=payload, vector=description_vector)
    qdrant_client.upsert(collection_name="question_tests", points=[point])

    return document_id

def delete_question_test(id_question_tests):
    # Delete a file from firebase storage
    question_tests_file_name = get_question_test_by_id(id_question_tests)["question_tests_file_name"]
    remove_file_question_tests(question_tests_file_name)
    # Delete a document by id_question_tests
    firebase_db.collection("question_tests").document(id_question_tests).delete()

    # Delete corresponding vector from Qdrant
    delete_result = qdrant_client.delete(
        collection_name="question_tests",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="id",
                        match=models.MatchValue(value=id_question_tests),
                    ),
                ],
            )
        ),
    )
    return delete_result
