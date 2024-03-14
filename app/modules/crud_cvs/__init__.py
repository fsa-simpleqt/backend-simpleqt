from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.crud_cvs.models.crud_cvs import get_all_cvs, create_cv, delete_cv

crud_cvs_router = APIRouter(prefix="/crud_cvs_router", tags=["crud_cvs_router"])

# [GET] all CVs
@crud_cvs_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_cvs()
    return data

# [POST] add CV
@crud_cvs_router.post("/")
# only upload pdf or docx file
async def add_cv(name_candidate: str, apply_position: str, file_cv: Annotated[UploadFile, File(..., description="Upload cv file (upload .pdf or .docx file)")]):
    try:
        # take file_cv and cv_upload type file
        file_cv_type = file_cv.filename.split(".")[-1]
        if file_cv_type in ["pdf", "docx"]:
            # create a new document
            if create_cv({"name_candidate": name_candidate, "apply_position":apply_position, "cv_content": file_cv}):
                return {"message": "CV added successfully"}
            else:
                return {"message": "Error while adding CV file to database"}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] CV by id
@crud_cvs_router.delete("/{id}")
async def delete_cv_by_id(id: str):
    # Delete a document by id
    if delete_cv(id):
        return {"message": f"CV have id {id} deleted successfully"}
    else:
        return {"message": "Error while deleting CV file from database"}