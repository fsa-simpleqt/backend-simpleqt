import json
from fastapi import APIRouter, Form, HTTPException

from app.modules.matching_cv.models.matching_cv_model import MatchingModel
from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd, check_config_score
from app.modules.crud_cvs.models.crud_cvs import get_cv_by_id
from app.modules.crud_jds.models.crud_jds import get_jd_by_id

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
async def matching_cv_jd(matching_data: MatchingModel):
    try:
        # check matching_data.config_score
        if matching_data.config_score:
            check_config_score(matching_data.config_score)
        else:
            return HTTPException(status_code=400, detail="config_score is required")
        
        # get matched status in database
        matched_status = get_cv_by_id(matching_data.id_cv).get("matched_status")
        if matched_status:
            return {"message": "CV already matched with a JD"}
        else:
            id_cv_resulted, matched_result = result_matching_cv_jd(id_cv=matching_data.id_cv, id_jd=matching_data.id_jd, config_score= matching_data.config_score, start_matching= True)
            cv_data = get_cv_by_id(id_cv_resulted)
            return {"message": "Matched successfully", "cv_data": cv_data, "matched_result": matched_result}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

@cvmatching_router.post("/rematching")
async def rematching_cv_jd(matching_data: MatchingModel):
    try:
        # check matching_data.config_score
        if matching_data.config_score:
            check_config_score(matching_data.config_score)
        else:
            return HTTPException(status_code=400, detail="config_score is required")
        
        # get matched status in database
        matched_status = get_cv_by_id(matching_data.id_cv).get("matched_status")
        if matched_status:
            id_cv_resulted, matched_result = result_matching_cv_jd(id_cv=matching_data.id_cv, id_jd=matching_data.id_jd, config_score= matching_data.config_score, start_matching= False)
            cv_data = get_cv_by_id(id_cv_resulted)
            return {"message": "Rematched successfully", "matched_result": matched_result, "cv_data": cv_data}
        else:
            return {"message": "CV not matched with a JD yet"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")
