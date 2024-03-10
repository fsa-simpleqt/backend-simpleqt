from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.crud_question_test.models.crud_question_tests import get_all_question_tests, get_question_test_by_id, create_question_test, update_question_test, delete_question_test

crud_question_tests_router = APIRouter(prefix="/crud_question_tests_router", tags=["crud_question_tests_router"])

# [GET] all question tests
@crud_question_tests_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_question_tests()
    return data

# [POST] add question test
@crud_question_tests_router.post("/")
# only upload pdf or json file
async def add_question_test(description: str, role: str, file_question_tests: Annotated[UploadFile, File(..., description="The question test file", media_type=["application/pdf", "application/json"])]):
    try:
        # check if file is pdf or json
        if file_question_tests.content_type == "application/pdf":
            # create a new document
            if create_question_test({"description": description, "role": role, "question_tests": file_question_tests}):
                return {"message": "Question test added successfully"}
            else:
                return {"message": "Error"}
        elif file_question_tests.content_type == "application/json":
            # create a new document
            if create_question_test({"question_tests_description": description, "question_tests_role": role, "question_tests_url": file_question_tests}):
                return {"message": "Question test added successfully"}
            else:
                return {"message": "Error"}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] question test by id
@crud_question_tests_router.delete("/{id}")
async def delete_question_test_by_id(id: str):
    # Delete a document by id
    if delete_question_test(id):
        return {"message": f"Question test have id {id} deleted successfully"}
    else:
        return {"message": "Error"}