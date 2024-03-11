import uuid
from app.configs.database import firebase_bucket, firebase_db
from app.configs.qdrant_db import qdrant_client
from app.configs.qdrant_db import models
from app.modules.question_tests_retrieval.models.text2vector import text2vector


# CRUD operation
def upload_file_question_tests(file):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file.filename
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_file(file.file)
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_question_tests(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def get_all_question_tests():
    # Get all documents from the collection
    docs = firebase_db.collection("question_tests").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        data.append(doc_data)
    return data

def get_question_test_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("question_tests").document(id).get()
    return doc.to_dict()

def get_question_test_url_by_description(description):
    # Get a question_tests_url where question_tests_description is equal to description
    docs = firebase_db.collection("question_tests").where("question_tests_description", "==", description).stream()
    for doc in docs:
        return doc.to_dict()["question_tests_url"]
    return False


def create_question_test(data):
    # get file_question_tests
    file_question_tests = data["question_tests_url"]
    # upload file to firebase storage
    file_url = upload_file_question_tests(file_question_tests)
    # add file url to data
    data["question_tests_url"] = file_url
    question_tests_des = data["question_tests_description"]
    # Create a new document
    document_ref = firebase_db.collection("question_tests").add(data)
    document_id = document_ref[1].id

    # Upload vector to Qdrant
    collection_info = qdrant_client.get_collection('question_tests')
    points_count = collection_info.points_count
    description_vector = text2vector(question_tests_des)
    payload = {"id": document_id}
    point = models.PointStruct(id=points_count+1, payload=payload, vector=description_vector)
    qdrant_client.upsert(collection_name="question_tests", points=[point])

    return True

def update_question_test(id, data):
    # Update a document by id
    firebase_db.collection("question_tests").document(id).update(data)
    return True

def delete_question_test(id):
    # Delete a file from firebase storage
    file_url = get_question_test_by_id(id)["question_tests_url"]
    remove_file_question_tests(file_url)
    # Delete a document by id
    firebase_db.collection("question_tests").document(id).delete()
    return True
