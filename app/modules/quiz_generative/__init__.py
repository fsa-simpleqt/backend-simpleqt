from fastapi import APIRouter, UploadFile, File

from app.modules.quiz_generative.models.quiz_gen_logic import question_rag
from app.utils.summary_jd import summary_jd

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
        sumaryjd_text = summary_jd(jobdes)
        if question_rag(sumaryjd_text):
            return {"message": "Generate quiz success",
                    "quiz": question_rag(sumaryjd_text)}
        else:
            return {"message": "Please upload only .txt file", "error": str(e)}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}
