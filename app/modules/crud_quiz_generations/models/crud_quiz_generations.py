import uuid
import os
import pytz
from datetime import datetime
import json

from urllib.request import urlopen
from app.configs.database import firebase_bucket, firebase_db

# CRUD operation
def upload_file_quiz_generation(file_path):
    # upload file to firebase storage from file_path
    name_file = file_path.split("/")[-1]
    # upload file to folder "quiz_generations" in firebase storage
    blob = firebase_bucket.blob(f"quiz_generations/{name_file}")
    blob.upload_from_filename(file_path)
    blob.make_public()
    # return Download URL of the file
    return blob.public_url

def remove_file_quiz_generation(file_name):
    # remove file from firebase storage quiz_generation_file_name
    blob = firebase_bucket.blob("quiz_generations/" + file_name)
    blob.delete()
    return True

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
    doc = firebase_db.collection("quiz_generations").document(id_quiz_generation).get()
    # add id_quiz_generation to doc
    doc = doc.to_dict()
    doc["id_quiz_generation"] = id_quiz_generation
    # store the response of URL 
    response = urlopen(doc["quiz_generation_url"])
    data_quiz_generation_json = json.loads(response.read())
    doc["exam_data"] = data_quiz_generation_json
    return doc


def create_quiz_generation(data):
    # get data
    json_quiz_generation_tests = data["json_quiz_generation_tests"]
    id_jd = data["id_jd"]

    # Create a new file
    file_name = f"{id_jd}_quiz_generation.json"
    cache_path = f"tmp/{file_name}"
    with open(cache_path, "w") as file:
        file.write(json_quiz_generation_tests)

    # upload file to firebase storage
    file_url = upload_file_quiz_generation(cache_path)
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
    # add id_jd to firebase_save_data
    firebase_save_data["id_jd"] = id_jd
    # add vietnam_now to firebase_save_data
    firebase_save_data["created_at"] = vietnam_now
    # add quiz_generation_url to firebase_save_data
    firebase_save_data["quiz_generation_url"] = file_url
    # add file_name to firebase_save_data
    firebase_save_data["quiz_generation_file_name"] = file_name

    # Create a new document
    document_ref = firebase_db.collection("quiz_generations").add(firebase_save_data)
    id_quiz_generation = document_ref[1].id
    return id_quiz_generation

def delete_quiz_generation(id_quiz_generation):
    # delete file in firebase storage
    quiz_generation_file_name = get_quiz_generation_by_id(id_quiz_generation)["quiz_generation_file_name"]
    # delete file in firebase storage
    remove_file_quiz_generation(quiz_generation_file_name)
    # delete document in firebase firestore
    firebase_db.collection("quiz_generations").document(id_quiz_generation).delete()
    return True
