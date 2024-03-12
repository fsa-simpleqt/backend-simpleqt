from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.question_tests_retrieval.models.jd2text import jobdes2text
# from app.modules.question_tests_retrieval.models.text2vector import text2vector
from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd")
# only upload .txt file
async def send_jd(txt_file: Annotated[UploadFile, File(..., description="The JD file (only .txt file)", media_type=["text/plain"])]):
    try:
        # read the txt file with format
        jobdes = txt_file.file.read().decode("utf-8")
        sumaryjd_text = jobdes2text(jobdes)
        if get_question_tests(sumaryjd_text):
            return {"message": "Send JD successfully and get question test successfully",
                    "sumaryjd_text": sumaryjd_text}
        else:
            return {"message": "Please upload only .txt file", "error": str(e)}
    except Exception as e:
        return {"message": "Please upload only .txt file", "error": str(e)}

