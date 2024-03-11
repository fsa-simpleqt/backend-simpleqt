import uuid
from app.configs.database import firebase_bucket, firebase_db

# CRUD operation
def upload_file_question_tests(file):
    re_name_file = str(uuid.uuid4()).replace("-","_") + "_" + file.filename
    # upload file to firebase storage
    blob = firebase_bucket.blob(re_name_file)
    blob.upload_from_file(file.file)
    # return gs link
    return f"gs://{firebase_bucket.name}/{re_name_file}"

def remove_file_question_tests(file_url):
    # remove file from firebase storage using "gs://" link
    blob = firebase_bucket.blob(file_url.split(f"gs://{firebase_bucket.name}/")[1])
    blob.delete()
    return True

def get_all_question_tests():
    # Get all documents from the collection
    docs = firebase_db.collection("question_tests").stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        data.append(doc_data)
    return data

def get_question_test_by_id(id):
    # Get a document by id
    doc = firebase_db.collection("question_tests").document(id).get()
    return doc.to_dict()

def get_question_test_url_by_description(description):
    # Get a question_tests_url where question_tests_description is equal to description
    docs = firebase_db.collection("question_tests").where("question_tests_description", "==", description).stream()
    for doc in docs:
        return doc.to_dict()["question_tests_url"]
    return False


def create_question_test(data):
    # get file_question_tests
    file_question_tests = data["question_tests_url"]
    # upload file to firebase storage
    file_url = upload_file_question_tests(file_question_tests)
    # add file url to data
    data["question_tests_url"] = file_url
    # Create a new document
    firebase_db.collection("question_tests").add(data)
    return True

def update_question_test(id, data):
    # Update a document by id
    firebase_db.collection("question_tests").document(id).update(data)
    return True

def delete_question_test(id):
    # Delete a file from firebase storage
    file_url = get_question_test_by_id(id)["question_tests"]
    remove_file_question_tests(file_url)
    # Delete a document by id
    firebase_db.collection("question_tests").document(id).delete()
    return True
