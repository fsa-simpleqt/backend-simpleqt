from fastapi import APIRouter, UploadFile, File
from typing import Annotated

cvmatching_router = APIRouter(prefix="/cvmatching", tags=["cvmatching"])

@cvmatching_router.get("/")
async def index():
    return {"message": "Welcome to CV matching page"}