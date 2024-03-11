from fastapi import APIRouter, UploadFile, File

class Match_JD_CV_Model:
    jd = UploadFile
    jd_default = File(..., description="Upload JD file", media_type=["text/plain"])
    cv = UploadFile
    cv_default = File(..., description="Upload CV file", media_type=["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"])