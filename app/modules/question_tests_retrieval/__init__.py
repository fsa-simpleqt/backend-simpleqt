from fastapi import APIRouter

from app.modules.question_tests_retrieval.models.jd2text import jobdes2text
from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_by_id, get_jd_text_by_id

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd_to_get_question")
# only upload .txt file
async def send_jd_to_get_question(id_jd: str):
    try:
        # get jd_text by id
        jd_text = get_jd_text_by_id(id_jd)
        sumaryjd_text = jobdes2text(jd_text)
        if get_question_tests(sumaryjd_text):
            return {"message": "Send JD successfully and get question test successfully",
                    "sumary JD": sumaryjd_text}
        else:
            return {"error": str(e)}
    except Exception as e:
        return {"message": "Have error when find JD in database", "error": str(e)}
