from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.crud_rag_question_tests.models.crud_rag_question_tests import get_all_rag_question_tests, create_rag_question_test, delete_question_test

crud_rag_question_tests_router = APIRouter(prefix="/crud_rag_question_tests_router", tags=["crud_rag_question_tests_router"])

# [GET] all question tests
@crud_rag_question_tests_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_rag_question_tests()
    return data

# [POST] add question test
@crud_rag_question_tests_router.post("/")
# only upload pdf or json file
async def add_question_generator(id_jd: str, file_question_generator_tests: Annotated[UploadFile, File(..., description="The question generator test file", media_type=["application/json"])]):
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
@crud_rag_question_tests_router.delete("/{id}")
async def delete_question_test_by_id(id: str):
    # Delete a document by id
    if delete_question_test(id):
        return {"message": f"Question test have id {id} deleted successfully"}
    else:
        return {"message": "Error"}