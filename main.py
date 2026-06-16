import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is online"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    # Save the file to a temp directory
    with open(f"/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Success", "filename": file.filename}

@app.post("/analyze")
async def analyze_video(filename: str = Form(...)):
    # This matches the endpoint your JS is calling
    return {"status": "analyzed", "filename": filename}