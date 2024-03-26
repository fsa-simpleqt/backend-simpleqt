import os
from fastapi import APIRouter,HTTPException
from fastapi.responses import FileResponse
import threading
import time

from app.configs.database import firebase_bucket

# crud import
from app.modules.crud_jds import crud_jds_router
from app.modules.crud_cvs import crud_cvs_router
from app.modules.crud_question_test import crud_question_tests_router
from app.modules.crud_rag_question_tests import crud_rag_question_tests_router
from app.modules.question_rag import quiz_gen_router
from app.modules.question_tests_retrieval import qtretrieval_router
from app.modules.matching_cv import cvmatching_router

modules_router = APIRouter(prefix="/modules", tags=["modules"])
modules_router.include_router(crud_jds_router)
modules_router.include_router(crud_cvs_router)
modules_router.include_router(qtretrieval_router)
modules_router.include_router(cvmatching_router)
modules_router.include_router(crud_question_tests_router)
modules_router.include_router(crud_rag_question_tests_router)
modules_router.include_router(quiz_gen_router)

def delete_file_after_delay(file_path, delay):
    time.sleep(delay)
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted.")

@modules_router.get("/")
async def index():
    return {"message": "Welcome to modules page"}

# download from "gs://" link
@modules_router.get("/download_file_gs_link")
async def download_file_gs_link(gs_link:str):
    # Get the blob name from the gs link
    file_name = gs_link.split(f"gs://{firebase_bucket.name}/")[1]
    blob = firebase_bucket.blob(file_name)
    # Download the file to a temporary location on the server
    temp_file = f'tmp/{file_name}'
    blob.download_to_filename(temp_file)
    # Return the file as a response
    response = FileResponse(temp_file, filename=file_name)
    # delete the file after 1 minutes
    threading.Thread(target=delete_file_after_delay, args=(temp_file, 60)).start()
    return response
