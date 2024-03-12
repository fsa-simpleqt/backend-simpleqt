import docx

from fastapi import APIRouter
from app.modules.matching_cv.models.match_cv_jd_model import Match_JD_CV_Model

from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
# only upload .pdf or .docx file
async def matching_cv_jd(id_jd: str, id_cv:str):
    try:
        pass
        # # take jd_upload and cv_upload type file
        # jd_upload_type = jd_upload.filename.split(".")[-1]
        # cv_upload_type = cv_upload.filename.split(".")[-1]
        # if jd_upload_type in ["txt"] and cv_upload_type in ["pdf", "docx"]:
        #     jd_text =  jd_upload.file.read().decode("utf-8")
        #     if cv_upload_type == "docx":
        #         cv_text = docx.Document(cv_upload.file).paragraphs
        #         cv_text = "\n".join([i.text for i in cv_text])
        #     elif cv_upload_type == "pdf":
        #         return {"message": "This feature is not available yet"}
        #     # check matching cv and jd
        #     result = result_matching_cv_jd(cv_text, jd_text)
        #     return {"result": result}
        # else:
        #     return {"message": "Please upload only .txt for JD. And .pdf or .docx file for CV"}
    except Exception as e:
        return {"Error": str(e)}
