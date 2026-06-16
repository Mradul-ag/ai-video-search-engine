import os
from fastapi import FastAPI, UploadFile, File
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
    return {"message": "Backend is running!"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    # Just return success for now to clear the '404' and 'Failed to fetch'
    return {"filename": file.filename, "status": "uploaded"}