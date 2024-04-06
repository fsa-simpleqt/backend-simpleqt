from fastapi import APIRouter, UploadFile, File, Form

from app.modules.crud_jds.models.crud_jds import get_all_jds, create_jd, delete_jd
from app.modules.crud_cvs.models.crud_cvs import get_all_cv_by_apply_jd_id, delete_cv

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
async def add_jd(position_applied_for: str = Form(...), file_jd: UploadFile = File(..., description="Upload jd file (upload .txt)")):
    try:
        file_jd_type = file_jd.filename.split(".")[-1]
        if file_jd_type in ["txt"]:
            # create a new document
            firebase_save_data = create_jd({"position_applied_for": position_applied_for,"jd_text_file": file_jd})
            return {"message": "JD added successfully",
                    "jd_data": firebase_save_data}
        else:
            return {"message": "File type not supported"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

# [DELETE] JD by id
@crud_jds_router.delete("/{id_jds}")
async def delete_jd_by_id(id_jds: str):
    
    # Get all CVs that apply for this JD
    cv_list = get_all_cv_by_apply_jd_id(id_jds)
    # check cv_list is not empty
    count_cv = len(cv_list)
    print(count_cv)
    if count_cv > 0:
        # Delete all CVs that apply for this JD
        for cv in cv_list:
            delete_cv(cv["id_cv"])
    # Delete a document by id
    if delete_jd(id_jds):
        return {"message": f"JD have id {id_jds} deleted successfully"}
    else:
        return {"message": "Error"}