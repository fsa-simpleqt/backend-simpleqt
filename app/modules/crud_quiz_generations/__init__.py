import json
from fastapi import APIRouter, HTTPException

from app.modules.crud_quiz_generations.models.crud_quiz_generations import get_all_quiz_generations, create_quiz_generation, delete_quiz_generation, get_quiz_generation_by_id
from app.modules.crud_quiz_generations.models.quiz_model import GenQuizModel

crud_quiz_generative_router = APIRouter(prefix="/crud_quiz_generative_router", tags=["crud_quiz_generative_router"])

# [GET] all question tests
@crud_quiz_generative_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_quiz_generations()
    return data

# # [POST] add question test
# @crud_quiz_generative_router.post("/")
# # only upload pdf or json file
# async def add_quiz_generation(gen_quiz_data: GenQuizModel):
#     try:
#         json_quiz_gen_data = json.dumps(gen_quiz_data.json_quiz_gen)
#         data_quiz_generation = {"id_jd": gen_quiz_data.id_jd, "json_quiz_generation_tests": json_quiz_gen_data}
#         id_quiz_generation = create_quiz_generation(data_quiz_generation)
#         quiz_gen_data = get_quiz_generation_by_id(id_quiz_generation)
#         return {"message": "Created generation question test successfully", "quiz_gen_data": quiz_gen_data}
#     except Exception as e:
#         return HTTPException(status_code=400, detail=f"{str(e)}")

# # [DELETE] question test by id
# @crud_quiz_generative_router.delete("/{id_quiz_generative}")
# async def delete_question_test_by_id(id_quiz_generative: str):
#     try:
#         # Delete a document by id
#         if delete_quiz_generation(id_quiz_generative):
#             return {"message": f"Question test have id {id_quiz_generative} deleted successfully"}
#     except Exception as e:
#         return HTTPException(status_code=400, detail=f"{str(e)}")
