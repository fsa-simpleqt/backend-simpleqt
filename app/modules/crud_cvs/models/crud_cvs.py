import uuid
import pytz
import io
import os

from app.configs.database import firebase_bucket, firebase_db
from docx import Document
from datetime import datetime

from langchain_community.document_loaders import UnstructuredPDFLoader
from app.modules.crud_jds.models.crud_jds import get_jd_by_id

# CRUD operation
def upload_file_cvs(file_path):
    # upload file to firebase storage from file_path
    name_file = file_path.split("/")[-1]
    blob = firebase_bucket.blob(name_file)
    blob.upload_from_filename(file_path)
    # return gs link
    return f"gs://{firebase_bucket.name}/{name_file}"

def remove_file_cvs(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def file_cv_doc2text(file_path):
    # Read the .docx file from file
    doc = Document(file_path)
    # Extract text from the .docx file
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# def load cv from docx file
def file_cv_pdf2text(file_path):
    # Read the .pdf file from the BytesIO object
    loader = UnstructuredPDFLoader(file_path)
    json_result = loader.load()
    # take page_content from json_result
    page_content  = json_result[0].page_content
    return page_content

def get_cv_content_by_id(id_cv):
    # Get a document by id
    doc = firebase_db.collection("cvs").document(id_cv).get()
    return doc.to_dict()["cv_content"]

def get_all_cvs():
    # Get all documents from the collection
    docs = firebase_db.collection("cvs").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_cv"] = doc.id
        apply_jd_id = doc_data.get("apply_jd_id")
        doc_data['apply_position'] = get_jd_by_id(apply_jd_id).get("position_applied_for")
        data.append(doc_data)
    return data

def get_cv_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("cvs").document(id).get()
    return doc.to_dict()

def create_cv(data):
    # get file_cv
    file_cv = data["cv_content"]
    # rename file name to uuid
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file_cv.filename
    # save uploaded file to tmp folder
    cache_path = f"tmp/{re_name_file}"
    with open(cache_path, "wb") as buffer:
        buffer.write(file_cv.file.read())
    
    # take file_cv and cv_upload type file
    file_cv_type = file_cv.filename.split(".")[-1]
    cv_text = ""
    if file_cv_type == "pdf":
        cv_text = file_cv_pdf2text(cache_path)
    elif file_cv_type == "docx":
        cv_text = file_cv_doc2text(cache_path)
    else:
        return False

    # upload file to firebase storage
    cv_uploaded_url = upload_file_cvs(cache_path)
    # delete file in tmp folder
    os.remove(cache_path)

    # Get the current time in UTC
    utc_now = datetime.now()
    # Specify the Vietnam time zone
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    # Convert the current time to Vietnam time zone
    vietnam_now = utc_now.replace(tzinfo=pytz.utc).astimezone(vietnam_timezone).strftime("%Y-%m-%d %H:%M:%S")

    # add file url to data
    data["cv_url"] = cv_uploaded_url
    # add cv_content
    data["cv_content"] = cv_text
    # add created_at
    data["created_at"] = vietnam_now
    # Create a new document
    firebase_db.collection("cvs").add(data)
    return True

def delete_cv(id):
    # Delete a file from firebase storage
    file_url = get_cv_by_id(id)["cv_url"]
    remove_file_cvs(file_url)
    # Delete a document by id
    firebase_db.collection("cvs").document(id).delete()
    return True
