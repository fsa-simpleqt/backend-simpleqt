from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.question_tests_retrieval.models.jd2text import jobdes2text
from app.modules.question_tests_retrieval.models.text2tector import text2vector
from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_test

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd")
# only upload .txt file
async def send_jd(txt_file: Annotated[UploadFile, File(..., description="The JD file", media_type=["text/plain"])]):
    try:
        # # read the txt file with format
        # jobdes = txt_file.file.read().decode("utf-8")
        # sumaryjd_text = jobdes2text(jobdes)
        # print("sumaryjd_text: ", sumaryjd_text)
        # sumaryjd_vector = text2vector(sumaryjd_text)
        # print("sumaryjd_vector: ", sumaryjd_vector)
        text = "Job Title is Senior AI Engineer, Level is Senior, and Brief summary of required skills is NLP, experiencing in using containers"
        if get_question_test(text):
            return {"message": "Send JD successfully and get question test successfully"}
        else:
            return {"message": "Error"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}