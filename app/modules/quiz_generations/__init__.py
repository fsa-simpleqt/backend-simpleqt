from fastapi import APIRouter, Form

from app.modules.quiz_generations.models.quiz_gen_logic import generate_question
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    return {"message": "Welcome to quiz generator page"}

@quiz_gen_router.post("/send_jd_to_gen_quiz")
async def quiz_gen(id_jd: str):
    try:
        sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        json_quiz_gen = generate_question(jobtext=sumaryjd_text)
        return {"message": "Generate question successfully", "json_quiz_gen": json_quiz_gen}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}

@quiz_gen_router.post("/add_gen_quiz_to_jd")
async def quiz_gen(id_jd: str = Form(...), json_quiz_gen: dict = Form(...)):
    pass