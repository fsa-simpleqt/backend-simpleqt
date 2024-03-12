import uuid
from app.configs.database import firebase_bucket, firebase_db


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
    file_jds = data["jd_url"]
    # upload file to firebase storage
    file_url = upload_file_jds(file_jds)
    # add file url to data
    data["jd_url"] = file_url
    # Create a new document
    document_ref = firebase_db.collection("jds").add(data)
    # document_id = document_ref[1].id
    return True

def delete_jd(id):
    # Delete a file from firebase storage
    file_url = get_jd_by_id(id)["jd_url"]
    remove_file_jds(file_url)
    # Delete a document by id
    firebase_db.collection("jds").document(id).delete()
    return True
