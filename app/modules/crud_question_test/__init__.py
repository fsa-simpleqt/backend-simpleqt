from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.modules.crud_question_test.models.crud_question_tests import get_all_question_tests, create_question_test, delete_question_test, get_question_test_by_id

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
            document_id = create_question_test({"question_tests_description": description, "file_question_tests": file_question_tests, "question_tests_upload_type": question_tests_upload_type})
            new_question_test = get_question_test_by_id(document_id)
            return {"message": "Question test added successfully", "question_tests_data": new_question_test}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

# [DELETE] question test by id
@crud_question_tests_router.delete("/{id_question_test}")
async def delete_question_test_by_id(id_question_test: str):
    try:
        # Delete a document by id
        if delete_question_test(id_question_test):
            return {"message": f"Question test have id {id_question_test} deleted successfully"}
        else:
            return {"message": "Error"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")