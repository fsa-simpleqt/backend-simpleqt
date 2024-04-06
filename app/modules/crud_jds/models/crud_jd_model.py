from pydantic import BaseModel 
from typing import List
from fastapi import Form, UploadFile, File

class CrudJDModel(BaseModel):
    position_applied_for: str = Form(...)
    jd_text_file: UploadFile = File(..., description="Upload jd file (upload .txt)")