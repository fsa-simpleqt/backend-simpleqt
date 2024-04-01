from fastapi import APIRouter, UploadFile, File

from app.modules.quiz_generations.models.quiz_gen_logic import generate_question
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    return {"message": "Welcome to quiz generator page"}

@quiz_gen_router.post("/quiz_gen")
async def quiz_gen(id_jd: str):
    try:
        sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        result = generate_question(jobtext=sumaryjd_text)
        return {"message": "Generate question successfully", "data": result}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}
