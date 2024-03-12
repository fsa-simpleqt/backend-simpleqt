import uuid
from app.configs.database import firebase_bucket, firebase_db

# CRUD operation
def upload_file_cvs(file):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file.filename
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_file(file.file)
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_cvs(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def download_file_cvs(file_url):
    # download file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    # download file and return string in file
    return blob.download_as_text()

def get_all_cvs():
    # Get all documents from the collection
    docs = firebase_db.collection("cvs").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_cv"] = doc.id
        data.append(doc_data)
    return data

def get_cv_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("cvs").document(id).get()
    return doc.to_dict()

def create_cv(data):
    # get file_cvs
    file_cvs = data["cv_url"]
    # upload file to firebase storage
    file_url = upload_file_cvs(file_cvs)
    # add file url to data
    data["cv_url"] = file_url
    # Create a new document
    document_ref = firebase_db.collection("cvs").add(data)
    # document_id = document_ref[1].id
    return True

def delete_cv(id):
    # Delete a file from firebase storage
    file_url = get_cv_by_id(id)["cv_url"]
    remove_file_cvs(file_url)
    # Delete a document by id
    firebase_db.collection("cvs").document(id).delete()
    return True
