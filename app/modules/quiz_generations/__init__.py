import json
from fastapi import APIRouter, Form, HTTPException

from app.modules.quiz_generations.models.quiz_gen_logic import generate_question
from app.modules.crud_jds.models.crud_jds import edit_jds, get_jd_by_id
from app.modules.crud_quiz_generations.models.crud_quiz_generations import create_quiz_generation, get_quiz_generation_by_id, delete_quiz_generation, get_all_quiz_generations
from app.modules.crud_quiz_generations.models.quiz_model import GenQuizModel

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    data_return = get_all_quiz_generations()
    return data_return

@quiz_gen_router.post("/send_jd_to_gen_quiz")
async def send_jd_to_gen_quiz(id_jd: str):
    try:
        # check if jd have question tests
        jd_have_question_tests = get_jd_by_id(id_jd).get("have_question_tests")
        if jd_have_question_tests:
            return HTTPException(status_code=400, detail="JD have question tests")
        
        sumaryjd_text = get_jd_by_id(id_jd=id_jd).get("jd_summary")
        json_quiz_gen = generate_question(jobtext=sumaryjd_text)
        return {"message": "Generate question successfully", "json_quiz_gen": json_quiz_gen}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@quiz_gen_router.put("/add_gen_quiz_to_jd")
async def add_gen_quiz_to_jd(gen_quiz_data: GenQuizModel):
    try:
        # check if jd have question tests
        jd_have_question_tests = get_jd_by_id(gen_quiz_data.id_jd).get("have_question_tests")
        if jd_have_question_tests:
            return HTTPException(status_code=400, detail="JD have question tests")
        
        # Add question tests to JD
        json_quiz_gen_data = json.dumps(gen_quiz_data.json_quiz_gen)
        data_quiz_generation = {"id_jd": gen_quiz_data.id_jd, "json_quiz_generation_tests": json_quiz_gen_data}
        id_quiz_generation = create_quiz_generation(data_quiz_generation)
        quiz_gen_data = get_quiz_generation_by_id(id_quiz_generation)

        # Update JD have_question_tests = True
        data_change = {"have_question_tests": True, "id_question_tests": id_quiz_generation, "is_generate_question_tests": True}
        if edit_jds(id_jd=gen_quiz_data.id_jd, data_change=data_change):
            return {"message": "Add question tests to JD successfully", "quiz_gen_data": quiz_gen_data}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@quiz_gen_router.delete("/delete_gen_quiz_in_jd")
async def delete_gen_quiz_in_jd(id_jd: str):
    try:
        # Delete gen_quiz in quiz_generations collection
        id_question_tests = get_jd_by_id(id_jd).get("id_question_tests")
        delete_quiz_generation(id_quiz_generation=id_question_tests)

        # Delete question tests in JD
        data_change = {"is_generate_question_tests": False, "have_question_tests": False, "id_question_tests": None}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Delete question tests in JD successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")
