import uuid
import pytz
import os

from app.configs.qdrant_db import qdrant_client, models
from app.configs.database import firebase_db
from datetime import datetime
from app.utils.summary_jd import summary_jd
from app.utils.text2vector import text2vector
from app.utils.jd_history import create_jd_history, remove_file_chat_history

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
    # add id_jd to doc_data
    doc_data = doc.to_dict()
    doc_data["id_jd"] = doc.id
    return doc_data

def get_jd_summary_by_id(id_jd: str):
    # Get a document by id
    doc = firebase_db.collection("jds").document(id_jd).get()
    return doc.to_dict()["jd_summary"]

def create_jd(data: dict):
    # get file_jds
    file_jds = data["jd_text_file"]
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

    # create a new document
    firebase_save_data = {}
    # add jd_text to firebase_save_data
    firebase_save_data["jd_text"] = jd_text
    # add jd_summary to firebase_save_data
    summary_jd_text = summary_jd(jd_text)
    firebase_save_data["jd_summary"] = summary_jd_text
    # add position_applied_for to firebase_save_data
    firebase_save_data["position_applied_for"] = data["position_applied_for"]
    # add created_at to firebase_save_data
    firebase_save_data["created_at"] = vietnam_now
    # add generate_question_tests to firebase_save_data
    firebase_save_data['is_generate_question_tests'] = False
    # add have_question_tests to firebase_save_data
    firebase_save_data['have_question_tests'] = False
    # add id_question_tests to firebase_save_data
    firebase_save_data['id_question_tests'] = None

    # Create a new document
    document_ref = firebase_db.collection("jds").add(firebase_save_data)
    document_id = document_ref[1].id
    
    # Upload vector to Qdrant
    collection_info = qdrant_client.get_collection('jds')
    points_count = collection_info.points_count
    summary_jd_vector = text2vector(summary_jd_text)
    payload = {"id_jd": document_id}
    point = models.PointStruct(id=points_count+1, payload=payload, vector=summary_jd_vector)
    qdrant_client.upsert(collection_name="jds", points=[point])

    # Create JD history
    history_save_data = {}
    chat_history_url, save_json_name = create_jd_history(summary_jd_text, document_id)
    # add chat_history_url to firebase_save_data
    history_save_data["chat_history_url"] = chat_history_url
    # add chat_history_file_name to firebase_save_data
    history_save_data["chat_history_file_name"] = save_json_name
    # Update a document
    firebase_db.collection("jds").document(document_id).update(history_save_data)

    return document_id

def edit_jds(id_jd: str, data_change: dict):
    # Update a document
    firebase_db.collection("jds").document(id_jd).update(data_change)

    return True

def delete_jd(id_jd: str):
    # Delete history of JD
    chat_history_file_name = get_jd_by_id(id_jd).get("chat_history_file_name")
    remove_file_chat_history(chat_history_file_name)
    # Delete a document by id
    firebase_db.collection("jds").document(id_jd).delete()
    # Delete corresponding vector from Qdrant
    delete_result = qdrant_client.delete(
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
    return delete_result
