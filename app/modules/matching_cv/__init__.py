import docx

from fastapi import APIRouter
# from app.modules.matching_cv.models.match_cv_jd_model import Match_JD_CV_Model

from app.modules.matching_cv.models.matching_cv_logic import result_matching_cv_jd
from app.modules.crud_jds.models.crud_jds import get_jd_by_id, file_jd_txt2text
from app.modules.crud_cvs.models.crud_cvs import get_cv_by_id, file_cv_doc2text

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}

@cvmatching_router.post("/matching")
# only upload .pdf or .docx file
async def matching_cv_jd(id_jd: str, id_cv:str):
    try:
        # get jd and cv by id
        jd_document = get_jd_by_id(id_jd)
        cv_document = get_cv_by_id(id_cv)

        # download file from firebase storage
        jd_url = jd_document["jd_url"]
        cv_url = cv_document["cv_url"]

        # get type file cv from cv_url "gs://bucket_name/file_name"
        cv_type = cv_url.split(".")[-1]
        if cv_type == "pdf":
            return {"message": "This feature is not available yet"}
        elif cv_type == "docx":
            cv_text = file_cv_doc2text(cv_url)
        else:
            return {"message": "Please upload only .pdf or .docx file for CV"}

        # get jd_text from jd_url "gs://bucket_name/file_name"
        jd_text = file_jd_txt2text(jd_url)

        result = result_matching_cv_jd(cv_text, jd_text)
        return {"result": result}
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
