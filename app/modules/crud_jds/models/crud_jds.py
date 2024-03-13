import uuid
from app.configs.database import firebase_bucket, firebase_db
from datetime import datetime
import pytz
import os

# CRUD operation
def upload_file_jds(file):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file.filename
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_file(file.file)
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_jds(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def get_jd_text_by_id(id_jd):
    # Get a document by id
    doc = firebase_db.collection("jds").document(id_jd).get()
    return doc.to_dict()["jd_text"]

def get_all_jds():
    # Get all documents from the collection
    docs = firebase_db.collection("jds").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_jd"] = doc.id
        data.append(doc_data)
    return data

def get_jd_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("jds").document(id).get()
    return doc.to_dict()

def create_jd(data):
    # get file_jds
    file_jds = data["jd_text"]
    # change file name to uuid
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file_jds.filename
    # save uploaded file to tmp folder
    with open(f"tmp/{re_name_file}", "wb") as buffer:
        buffer.write(file_jds.file.read())
    # read file
    with open(f"tmp/{re_name_file}", "r", encoding="utf8") as file:
        jd_text = file.read()
    # delete file in tmp folder
    os.remove(f"tmp/{re_name_file}")

    # # upload file to firebase storage
    # file_url = upload_file_jds(file_jds)

    # Get the current time in UTC
    utc_now = datetime.utcnow()
    # Specify the Vietnam time zone
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    # Convert the current time to Vietnam time zone
    vietnam_now = utc_now.replace(tzinfo=pytz.utc).astimezone(vietnam_timezone).strftime("%Y-%m-%d %H:%M:%S")

    # add file url to data
    data["jd_text"] = jd_text
    # add created_at
    data["created_at"] = vietnam_now
    # Create a new document
    firebase_db.collection("jds").add(data)
    return True

def delete_jd(id):
    # # Delete a file from firebase storage
    # file_url = get_jd_by_id(id)["jd_url"]
    # remove_file_jds(file_url)
    # Delete a document by id
    firebase_db.collection("jds").document(id).delete()
    return True
