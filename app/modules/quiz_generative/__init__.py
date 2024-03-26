from fastapi import APIRouter, UploadFile, File
from fastapi import APIRouter

from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id
from app.modules.crud_rag_question_tests.models.crud_rag_question_tests import download_file_rag_question_tests, get_all_rag_question_tests
from app.modules.quiz_generative.models.quiz_gen_logic import question_rag

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    data = get_all_rag_question_tests()
    return data

@quiz_gen_router.post("/quiz_gen")
async def quiz_gen(id_jd: str):
    try:
        # get jd_text from id_jd
        sumaryjd_text = get_jd_summary_by_id(id_jd)

        message = question_rag(sumaryjd_text=sumaryjd_text, id_jd= id_jd)
        return message
    except Exception as e:
        return {"message": str(e)}

@quiz_gen_router.post("/test_gen")
async def test_gen(url: str):
    download_file_rag_question_tests(url)
