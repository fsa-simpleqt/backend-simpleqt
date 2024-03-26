from fastapi import APIRouter

from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd_to_get_question")
async def send_jd_to_get_question(id_jd: str):
    try:
        # get jd_text by id
        sumaryjd_text = get_jd_summary_by_id(id_jd)
        result = get_question_tests(sumaryjd_text)
        return {"message": "Send JD successfully and get question test successfully",
                "result": result}
    except Exception as e:
        return {"message": "Have error when find JD in database", "error": str(e)}
