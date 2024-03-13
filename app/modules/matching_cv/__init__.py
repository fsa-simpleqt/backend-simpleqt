import docx

from fastapi import APIRouter
# from app.modules.matching_cv.models.match_cv_jd_model import Match_JD_CV_Model

from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd
from app.modules.crud_jds.models.crud_jds import get_jd_by_id, get_jd_text_by_id
from app.modules.crud_cvs.models.crud_cvs import get_cv_by_id, file_cv_doc2text, file_cv_pdf2text

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
# only upload .pdf or .docx file
async def matching_cv_jd(id_jd: str, id_cv:str):
    try:
        cv_content = get_cv_by_id(id_cv)
        jd_text = get_jd_text_by_id(id_jd)

        result = result_matching_cv_jd(cv_text=cv_content,jd_text=jd_text)
        return {"result": result}
    except Exception as e:
        return {"Error": str(e)}
