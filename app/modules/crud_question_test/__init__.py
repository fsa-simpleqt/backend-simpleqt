from fastapi import APIRouter, UploadFile, File, Form

from app.modules.crud_question_test.models.crud_question_tests import get_all_question_tests, create_question_test, delete_question_test

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
async def add_question_test(description: str = Form(...), file_question_tests: UploadFile = File(..., description="The question test file (Upload .pdf or .json)")):
    try:
        question_tests_upload_type = file_question_tests.filename.split(".")[-1]
        # check if file is pdf or json
        if question_tests_upload_type == "pdf" or question_tests_upload_type == "json":
            # create a new document
            if create_question_test({"question_tests_description": description, "file_question_tests": file_question_tests, "question_tests_upload_type": question_tests_upload_type}):
                return {"message": "Question test added successfully"}
            else:
                return {"message": "Error", "error": str(e)}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] question test by id
@crud_question_tests_router.delete("/{id}")
async def delete_question_test_by_id(id: str):
    try:
        # Delete a document by id
        if delete_question_test(id):
            return {"message": f"Question test have id {id} deleted successfully"}
        else:
            return {"message": "Error"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}