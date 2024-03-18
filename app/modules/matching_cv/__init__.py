import docx

from fastapi import APIRouter
# from app.modules.matching_cv.models.match_cv_jd_model import Match_JD_CV_Model

from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
# only upload .pdf or .docx file
async def matching_cv_jd(id_jd: str, id_cv:str):
    try:
        result = result_matching_cv_jd(id_cv=id_cv,id_jd=id_jd)
        return {"result": result}
    except Exception as e:
        return {"Error": str(e)}
