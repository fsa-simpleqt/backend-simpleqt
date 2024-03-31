import uuid
from app.configs.database import firebase_bucket, firebase_db

from datetime import datetime
import pytz

# CRUD operation
def upload_file_quiz_generative(file):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file.filename
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_file(file.file)
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_quiz_generative(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def get_all_quiz_generative():
    # Get all documents from the collection
    docs = firebase_db.collection("quiz_generative").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        data.append(doc_data)
    return data

def get_question_test_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("quiz_generative").document(id).get()
    return doc.to_dict()

def create_rag_question_test(data):
    # get file_quiz_generative
    file_quiz_generative = data["question_generator_tests_url"]
    # upload file to firebase storage
    file_url = upload_file_quiz_generative(file_quiz_generative)

    # Get the current time in UTC
    utc_now = datetime.now()
    # Specify the Vietnam time zone
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    # Convert the current time to Vietnam time zone
    vietnam_now = utc_now.replace(tzinfo=pytz.utc).astimezone(vietnam_timezone).strftime("%Y-%m-%d %H:%M:%S")
    # add created_at
    data["created_at"] = vietnam_now

    # add file url to data
    data["question_generator_tests_url"] = file_url
    # Create a new document
    document_ref = firebase_db.collection("quiz_generative").add(data)
    return True

def delete_question_test(id):
    # Delete a file from firebase storage
    file_url = get_question_test_by_id(id)["question_generator_tests_url"]
    remove_file_quiz_generative(file_url)
    # Delete a document by id
    firebase_db.collection("quiz_generative").document(id).delete()
    return True
