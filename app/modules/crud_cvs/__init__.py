from fastapi import APIRouter, UploadFile, File, Form

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
async def add_cv(apply_jd_id: str, files_cv: list[UploadFile] = File(..., description="Upload cv file (upload .pdf or .docx)")):
    try:
        count_sucessful = 0
        count_failed = 0
        for file_cv in files_cv:
            file_cv_type = file_cv.filename.split(".")[-1]
            if file_cv_type in ["pdf", "docx"]:
                # create a new document
                if create_cv({"apply_jd_id": apply_jd_id, "cv_content": file_cv}):
                    count_sucessful += 1
                else:
                    count_failed += 1
            else:
                count_failed += 1
        return {"message": "CVs added successfully",
                "count_sucessful": count_sucessful,
                "count_failed": count_failed}
    except Exception as e:
        return {"message": str(e)}

# [DELETE] CV by id
@crud_cvs_router.delete("/{id}")
async def delete_cv_by_id(id: str):
    # Delete a document by id
    if delete_cv(id):
        return {"message": f"CV have id {id} deleted successfully"}
    else:
        return {"message": "Error while deleting CV file from database"}