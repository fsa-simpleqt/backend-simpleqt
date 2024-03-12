import uuid
from app.configs.database import firebase_bucket, firebase_db
import io
from docx import Document

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

def file_cv_doc2text(file_url):
    # download file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    # download file and return string in file
    file_bytes = blob.download_as_bytes()
    # Create a BytesIO object from the file bytes
    file_stream = io.BytesIO(file_bytes)
    # Read the .docx file from the BytesIO object
    doc = Document(file_stream)
    # Extract text from the .docx file
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text


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
