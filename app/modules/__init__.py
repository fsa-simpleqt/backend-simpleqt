from fastapi import APIRouter
from app.modules.question_retrieval import qtretrieval_router

modules_router = APIRouter(prefix="/modules", tags=["modules"])
modules_router.include_router(qtretrieval_router)

@modules_router.get("/")
async def index():
    return {"message": "Welcome to modules page"}