import uuid
from app.configs.database import firebase_bucket, firebase_db

from datetime import datetime
import pytz

# CRUD operation
def upload_file_quiz_generation(file):
    pass

def remove_file_quiz_generation(file_path):
    pass

def get_all_quiz_generations():
    # Get all documents from the collection
    docs = firebase_db.collection("quiz_generations").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_quiz_generation"] = doc.id
        data.append(doc_data)
    return data

def get_quiz_generation_by_id(id_quiz_generation: str):
    # Get a document by id
    doc = firebase_db.collection("quiz_generations").document(id).get()
    return doc.to_dict()

def create_quiz_generation(data):
    # get file_quiz_generations
    file_quiz_generations = data["question_generator_tests_url"]
    # upload file to firebase storage
    file_url = upload_file_quiz_generation(file_quiz_generations)

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
    document_ref = firebase_db.collection("quiz_generations").add(data)
    return True

def delete_quiz_generation(id):
    pass
