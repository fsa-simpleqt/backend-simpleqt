from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.question_rag.models.question_rag_logic import question_rag
from app.modules.question_tests_retrieval.models.jd2text import jobdes2text

quiz_gen_router = APIRouter(prefix="/quiz_gen", tags=["quiz_gen"])

@quiz_gen_router.get("/")
async def index():
    return {"message": "Welcome to quiz generator page"}

@quiz_gen_router.post("/quiz_gen")
# only upload .txt file
async def quiz_gen(txt_file: UploadFile = File(..., description="The JD file (only .txt file)")):
    try:
        # read the txt file with format
        jobdes = txt_file.file.read().decode("utf-8")
        sumaryjd_text = jobdes2text(jobdes)
        if question_rag(sumaryjd_text):
            return {"message": "Generate quiz success",
                    "quiz": question_rag(sumaryjd_text)}
        else:
            return {"message": "Please upload only .txt file", "error": str(e)}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}
