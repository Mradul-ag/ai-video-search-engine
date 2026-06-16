import os
from fastapi import FastAPI, UploadFile, File
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
def health_check():
    return {"status": "online"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Simple save to memory/temp location
    with open(f"/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Success", "filename": file.filename}

@app.post("/analyze")
async def analyze(filename: str):
    # This matches the endpoint your JS is calling
    return {"message": "Analyzed", "filename": filename, "segments": 5}