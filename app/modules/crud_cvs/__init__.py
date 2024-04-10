from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.modules.crud_cvs.models.crud_cvs import get_all_cvs, create_cv, delete_cv, get_cv_by_id

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
async def add_cv(apply_jd_id: str = Form(...), files_cv: list[UploadFile] = File(..., description="Upload cv file (upload .pdf or .docx)")):
    try:
        count_sucessful = 0
        count_failed = 0
        cv_list = []
        for file_cv in files_cv:
            file_cv_type = file_cv.filename.split(".")[-1]
            if file_cv_type in ["pdf", "docx", "doc", "PDF", "DOCX", "DOC"]:
                # create a new document
                document_id = create_cv({"apply_jd_id": apply_jd_id, "cv_content": file_cv})
                new_cv = get_cv_by_id(document_id)
                cv_list.append(new_cv)
                count_sucessful += 1
            else:
                count_failed += 1
                next
        return {"message": "CVs added successfully",
                "count_sucessful": count_sucessful,
                "count_failed": count_failed,
                "cv_list": cv_list}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")

# [DELETE] CV by id
@crud_cvs_router.delete("/{id_cvs}")
async def delete_cv_by_id(id_cvs: str):
    try:
        # Delete a document by id
        if delete_cv(id_cvs):
            return {"message": f"CV have id {id_cvs} deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{str(e)}")
