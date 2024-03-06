from fastapi import APIRouter, UploadFile

qtretrieval_router = APIRouter(prefix="/qtretrieval", tags=["qtretrieval"])

@qtretrieval_router.get("/")
async def index():
    return {"message": "Welcome to question retrieval page"}