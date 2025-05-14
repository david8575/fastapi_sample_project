from fastapi import APIRouter, File, UploadFile
from typing import Dict
import os
import shutil

router = APIRouter(
    prefix="/upload", 
    tags=["upload"]
)

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": save_path
    }
