from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated

from app.modules.crud_quiz_generations.models.crud_quiz_generations import get_all_quiz_generations, create_quiz_generation, delete_quiz_generation

crud_quiz_generative_router = APIRouter(prefix="/crud_quiz_generative_router", tags=["crud_quiz_generative_router"])

# [GET] all question tests
@crud_quiz_generative_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_quiz_generations()
    return data

# [POST] add question test
@crud_quiz_generative_router.post("/")
# only upload pdf or json file
async def add_quiz_generation(json_quiz_generation_tests: dict = Form(...), id_jd: str = Form(...)):
    try:
        data_quiz_generation = {"id_jd": id_jd, "json_quiz_generation_tests": json_quiz_generation_tests}
        create_quiz_generation(data_quiz_generation)
        return {"message": "Created generation question test successfully"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] question test by id
@crud_quiz_generative_router.delete("/{id_quiz_generative}")
async def delete_question_test_by_id(id_quiz_generative: str):
    # Delete a document by id
    if delete_quiz_generation(id_quiz_generative):
        return {"message": f"Question test have id {id_quiz_generative} deleted successfully"}
    else:
        return {"message": "Error"}