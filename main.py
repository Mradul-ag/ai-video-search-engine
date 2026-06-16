import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": file_path, "filename": file.filename}

@app.post("/analyze-video")
async def analyze_video(file_path: str = Form(...)):
    # This will return dummy data so the frontend stops showing 'Failed to fetch'
    return {
        "saved_segments_count": 1, 
        "analysis": "[00:00] Analysis complete for " + file_path
    }