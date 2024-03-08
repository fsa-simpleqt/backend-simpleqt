from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.question_retrieval.models.jd2text import jobdes2text

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}

@qtretrieval_router.post("/send_jd")
# only upload .txt file
async def send_jd(txt_file: Annotated[UploadFile, File(..., description="The JD file", media_type=["text/plain"])]):
    try:
        # read the txt file with format
        jobdes = txt_file.file.read().decode("utf-8")
        result = jobdes2text(jobdes)
        return {"message": "Send JD successfully", "text": result}
    except Exception as e:
        return {"message": "Error", "error": "Please check the file format or the file content. The file should be .txt format."}
