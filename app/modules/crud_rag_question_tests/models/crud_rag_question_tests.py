import uuid
from app.configs.database import firebase_bucket, firebase_db
import json
import os
import threading
import time

from datetime import datetime
import pytz

def delete_file_after_delay(file_path, delay):
    time.sleep(delay)
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted.")

# CRUD operation
def upload_file_rag_question_tests(data_dict):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_gen_questions.json"
    cache_path = f"tmp/{re_name_file}"
    # upload file to firebase storage
    with open(cache_path, "w") as outfile:
        json.dump(data_dict, outfile)
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_filename(cache_path)
    # # delete cache
    # os.remove(cache_path)
    # delete the file after 10 second
    threading.Thread(target=delete_file_after_delay, args=(cache_path, 10)).start()
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_rag_question_tests(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def download_file_rag_question_tests(file_url):
    file_name = file_url.split(f"gs://{firebase_bucket.name}/")[1]
    cache_path = f"tmp/{file_name}"
    blob = firebase_bucket.blob(file_name)
    blob.download_to_filename(cache_path)
    return True

def get_all_rag_question_tests():
    # Get all documents from the collection
    docs = firebase_db.collection("rag_question_tests").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        data.append(doc_data)
    return data

def get_question_test_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("rag_question_tests").document(id).get()
    return doc.to_dict()

def create_rag_question_test(data):
    # get file_rag_question_tests
    dict_rag_question_tests = data["question_generator_tests_url"] 
    # upload file to firebase storage
    file_url = upload_file_rag_question_tests(dict_rag_question_tests)

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
    firebase_db.collection("rag_question_tests").add(data)
    return True

def delete_question_test(id):
    # Delete a file from firebase storage
    file_url = get_question_test_by_id(id)["question_generator_tests_url"]
    remove_file_rag_question_tests(file_url)
    # Delete a document by id
    firebase_db.collection("rag_question_tests").document(id).delete()
    return True
