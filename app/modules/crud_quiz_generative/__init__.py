from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated

from app.modules.crud_quiz_generative.models.crud_quiz_generative import get_all_quiz_generative, create_rag_question_test, delete_question_test

crud_quiz_generative_router = APIRouter(prefix="/crud_quiz_generative_router", tags=["crud_quiz_generative_router"])

# [GET] all question tests
@crud_quiz_generative_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_quiz_generative()
    return data

# [POST] add question test
@crud_quiz_generative_router.post("/")
# only upload pdf or json file
async def add_question_generator(id_jd: str, file_question_generator_tests: UploadFile = File(..., description="The question generator test file")):
    try:
        question_tests_upload_type = file_question_generator_tests.filename.split(".")[-1]
        # check if file is json
        if question_tests_upload_type == "json":
            # create a new document
            if create_rag_question_test({"id_jd": id_jd, "question_generator_tests_url": file_question_generator_tests}):
                return {"message": "Question test added successfully"}
            else:
                return {"error": str(e)}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] question test by id
@crud_quiz_generative_router.delete("/{id}")
async def delete_question_test_by_id(id: str):
    # Delete a document by id
    if delete_question_test(id):
        return {"message": f"Question test have id {id} deleted successfully"}
    else:
        return {"message": "Error"}