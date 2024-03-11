from fastapi import APIRouter
from app.modules.question_tests_retrieval import qtretrieval_router
from app.modules.crud_question_test import crud_question_tests_router
from app.modules.matching_cv import cvmatching_router

modules_router = APIRouter(prefix="/modules", tags=["modules"])
modules_router.include_router(qtretrieval_router)
modules_router.include_router(crud_question_tests_router)
modules_router.include_router(cvmatching_router)

@modules_router.get("/")
async def index():
    return {"message": "Welcome to modules page"}