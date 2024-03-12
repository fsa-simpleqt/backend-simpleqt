from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.question_tests_retrieval.models.jd2text import jobdes2text
from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_by_id, file_jd_txt2text

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd_to_get_question")
# only upload .txt file
async def send_jd_to_get_question(id_jd: str):
    try:
        jd_document = get_jd_by_id(id_jd)
        # download jd file from firebase storage
        jd_file_string = file_jd_txt2text(jd_document["jd_url"])
        sumaryjd_text = jobdes2text(jd_file_string)
        if get_question_tests(sumaryjd_text):
            return {"message": "Send JD successfully and get question test successfully",
                    "sumaryjd_text": sumaryjd_text}
        else:
            return {"message": "Please upload only .txt file", "error": str(e)}
    except Exception as e:
        return {"message": "Have error when find JD in database", "error": str(e)}

