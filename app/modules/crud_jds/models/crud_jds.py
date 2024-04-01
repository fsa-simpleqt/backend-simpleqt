import uuid
import pytz
import os

from app.configs.qdrant_db import qdrant_client, models
from app.configs.database import firebase_db
from datetime import datetime
from app.utils.summary_jd import summary_jd
from app.utils.text2vector import text2vector
from app.utils.jd_history import create_jd_history

def get_all_jds():
    # Get all documents from the collection
    docs = firebase_db.collection("jds").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id_jd"] = doc.id
        data.append(doc_data)
    return data

def get_jd_by_id(id_jd: str):
    # Get a document by id
    doc = firebase_db.collection("jds").document(id_jd).get()
    return doc.to_dict()

def get_jd_summary_by_id(id_jd: str):
    # Get a document by id
    doc = firebase_db.collection("jds").document(id_jd).get()
    return doc.to_dict()["jd_summary"]

def create_jd(data: dict):
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

    # Get the current time in UTC
    utc_now = datetime.now()
    # Specify the Vietnam time zone
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    # Convert the current time to Vietnam time zone
    vietnam_now = utc_now.replace(tzinfo=pytz.utc).astimezone(vietnam_timezone).strftime("%Y-%m-%d %H:%M:%S")

    data["jd_text"] = jd_text
    summary_jd_text = summary_jd(jd_text)
    data["jd_summary"] = summary_jd_text
    # add created_at
    data["created_at"] = vietnam_now
    # add generate_question_tests
    data['is_generate_question_tests'] = False
    # add have_question_tests
    data['have_question_tests'] = False
    # add id_question_tests
    data['id_question_tests'] = None
    # Create a new document
    document_ref = firebase_db.collection("jds").add(data)
    document_id = document_ref[1].id
    
    # Upload vector to Qdrant
    collection_info = qdrant_client.get_collection('jds')
    points_count = collection_info.points_count
    summary_jd_vector = text2vector(summary_jd_text)
    payload = {"id_jd": document_id}
    point = models.PointStruct(id=points_count+1, payload=payload, vector=summary_jd_vector)
    qdrant_client.upsert(collection_name="jds", points=[point])

    # Create JD history
    create_jd_history(summary_jd_text, document_id)
    return True

def edit_jds(id_jd: str, data_change: dict):
    # Update a document
    firebase_db.collection("jds").document(id_jd).update(data_change)

    return True

def delete_jd(id_jd: str):
    # Delete history of JD
    os.remove(f"data/chat_history/{id_jd}_chat_history.json")
    # Delete a document by id
    firebase_db.collection("jds").document(id_jd).delete()
    # Delete corresponding vector from Qdrant
    qdrant_client.delete(
        collection_name="jds",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="id",
                        match=models.MatchValue(value=id_jd),
                    ),
                ],
            )
        ),
    )
    return True
