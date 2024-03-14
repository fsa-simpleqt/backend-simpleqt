from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from app.modules.crud_jds.models.crud_jds import get_all_jds, create_jd, delete_jd

crud_jds_router = APIRouter(prefix="/crud_jds_router", tags=["crud_jds_router"])

# [GET] all JDs
@crud_jds_router.get("/")
async def index():
    # Get all documents from the collection with id document
    data = get_all_jds()
    return data

# [POST] add JD
@crud_jds_router.post("/")
# only upload txt file
async def add_jd(position_applied_for: str, file_jd: Annotated[UploadFile, File(..., description="Upload jd file (upload .txt)")]):
    try:
        file_jd_type = file_jd.filename.split(".")[-1]
        if file_jd_type in ["txt"]:
            # create a new document
            if create_jd({"position_applied_for": position_applied_for,"jd_text": file_jd}):
                return {"message": "JD added successfully"}
            else:
                return {"message": "Error while adding JD file to database"}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] JD by id
@crud_jds_router.delete("/{id}")
async def delete_jd_by_id(id: str):
    # Delete a document by id
    if delete_jd(id):
        return {"message": f"JD have id {id} deleted successfully"}
    else:
        return {"message": "Error"}