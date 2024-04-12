from fastapi import APIRouter

from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id, edit_jds

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.post("/send_jd_to_get_question")
# only upload .txt file
async def send_jd_to_get_question(id_jd: str):
    try:
        # get jd_text by id
        sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        result = get_question_tests(sumaryjd_text)
        return {"message": result}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

@qtretrieval_router.put("/add_get_question_to_jd")
async def add_get_question_to_jd(id_jd: str, id_question_tests:str):
    try:
        data_change = {"is_generate_question_tests": False, "have_question_tests": True, "id_question_tests": id_question_tests}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Add question tests to JD successfully"}
        else:
            return {"message": "Error"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}
