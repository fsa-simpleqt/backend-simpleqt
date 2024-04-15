from fastapi import APIRouter, Form, HTTPException

from app.modules.question_tests_retrieval.models.question_tests_logic import get_question_tests
from app.modules.crud_jds.models.crud_jds import get_jd_summary_by_id, edit_jds, get_jd_by_id
from app.modules.crud_question_test.models.crud_question_tests import get_question_test_by_id, get_question_test_data_by_id
from app.modules.crud_quiz_generations.models.crud_quiz_generations import get_quiz_generation_by_id

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.post("/send_jd_to_get_question_tests")
# only upload .txt file
async def send_jd_to_get_question(id_jd: str):
    try:
        # check if jd have question tests
        jd_have_question_tests = get_jd_by_id(id_jd).get("have_question_tests")
        if jd_have_question_tests:
            return HTTPException(status_code=400, detail="JD have question tests")
        
        # get jd_text by id
        sumaryjd_text = get_jd_summary_by_id(id_jd=id_jd)
        data_question_tests = get_question_tests(sumaryjd_text)
        return {"message": "Get question tests successfully", "data_question_tests": data_question_tests}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@qtretrieval_router.put("/add_get_question_tests_to_jd")
async def add_get_question_to_jd(id_jd: str, id_question_tests:str):
    try:
        # check if jd have question tests
        jd_have_question_tests = get_jd_by_id(id_jd).get("have_question_tests")
        if jd_have_question_tests:
            return HTTPException(status_code=400, detail="JD have question tests")
        
        data_change = {"is_generate_question_tests": False, "have_question_tests": True, "id_question_tests": id_question_tests}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Add question tests to JD successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@qtretrieval_router.delete("/delete_question_tests_in_jd")
async def delete_question_tests_in_jd(id_jd: str):
    try:
        # check is_generate_question_tests = False
        is_generate_question_tests = get_jd_by_id(id_jd).get("is_generate_question_tests")
        if is_generate_question_tests:
            return HTTPException(status_code=400, detail="JD is generate question tests")
        
        data_change = {"is_generate_question_tests": False, "have_question_tests": False, "id_question_tests": None}
        if edit_jds(id_jd=id_jd, data_change=data_change):
            return {"message": "Delete question tests in JD successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@qtretrieval_router.get("/get_exam_data_by_jd")
async def get_exam_data_by_jd(id_jd: str):
    try:
        have_question_tests = get_jd_by_id(id_jd).get("have_question_tests")
        id_question_tests = get_jd_by_id(id_jd).get("id_question_tests")
        if have_question_tests:
            is_generate_question_tests = get_jd_by_id(id_jd).get("is_generate_question_tests")
            if is_generate_question_tests:
                test_data = get_quiz_generation_by_id(id_question_tests)
                return test_data
            else:
                doc = get_question_test_by_id(id_question_tests)
                doc_name = doc.get("question_tests_file_name")
                doc_name_ext = doc_name.split(".")[-1]
                if doc_name_ext == "pdf":
                    return doc
                else:
                    test_data = get_question_test_data_by_id(id_question_tests)
                    return test_data
        else:
            return HTTPException(status_code=400, detail=f"No data")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")