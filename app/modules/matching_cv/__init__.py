from fastapi import APIRouter

from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd, matchingcv_testzone
from app.modules.crud_cvs.models.crud_cvs import get_cv_by_id
from app.modules.crud_jds.models.crud_jds import get_jd_by_id

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
async def matching_cv_jd(id_jd: str, id_cv:str):
    try:
        data_cv = get_cv_by_id(id_cv)
        # get matched status in database
        matched_status = data_cv.get("matched_status")
        if matched_status:
            return {"message": "CV already matched with a JD"}
        else:
            matched_result = result_matching_cv_jd(id_cv=id_cv,id_jd=id_jd)
            return {"message": "Matched successfully", "matched_result": matched_result}
    except Exception as e:
        return {"Error": str(e)}

@cvmatching_router.post("/rematching")
async def rematching_cv_jd(id_jd: str, id_cv:str):
    try:
        data_cv = get_cv_by_id(id_cv)
        # get matched status in database
        matched_status = data_cv.get("matched_status")
        if matched_status:
            result_dict = result_matching_cv_jd(id_cv=id_cv,id_jd=id_jd)
            return {"message": "Rematched successfully", "result_dict": result_dict}
        else:
            return {"message": "CV not matched with a JD yet"}
    except Exception as e:
        return {"Error": str(e)}

@cvmatching_router.post("/matchingcv_testzone")
async def matching_cv_jd_testzone(id_jd: str, id_cv:str):
    pass