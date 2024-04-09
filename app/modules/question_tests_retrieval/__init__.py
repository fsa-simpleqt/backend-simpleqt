from fastapi import APIRouter, Form, Response, status, HTTPException

from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id, edit_jds

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.post("/send_jd_to_get_question_tests", status_code=status.HTTP_200_OK)
# only upload .txt file
async def send_jd_to_get_question(id_jd: str = Form(...)):
    try:
        # get jd_text by id
        sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        result = get_question_tests(sumaryjd_text)
        return {"message": result}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@qtretrieval_router.put("/add_get_question_tests_to_jd", status_code=status.HTTP_200_OK)
async def add_get_question_to_jd(id_jd: str = Form(...), id_question_tests:str = Form(...)):
    try:
        data_change = {"is_generate_question_tests": False, "have_question_tests": True, "id_question_tests": id_question_tests}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Add question tests to JD successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@qtretrieval_router.put("/delete_question_tests_in_jd", status_code=status.HTTP_200_OK)
async def delete_question_tests_in_jd(id_jd: str = Form(...)):
    try:
        data_change = {"is_generate_question_tests": False, "have_question_tests": False, "id_question_tests": None}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Delete question tests in JD successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")
