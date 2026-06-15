import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.genai as google_genai
import chromadb
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploaded_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ⚠️ Gemini Client
# Replace your hardcoded API key string with this line:
api_key = os.environ.get("GEMINI_API_KEY")
client = google_genai.Client(api_key=GEMINI_API_KEY)

# 💾 Initialize ChromaDB in RAM Memory (Bypasses all OneDrive/Windows file locks!)
import chromadb
chroma_client = chromadb.EphemeralClient()

try:
    collection = chroma_client.get_collection(name="video_segments")
    print("🧠 ChromaDB virtual RAM allocation connected successfully!")
except Exception:
    collection = chroma_client.create_collection(name="video_segments")
    print("✨ Fresh, lightning-fast virtual vector workspace initialized!")


@app.post("/upload-video")
async def receive_video(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze-video")
async def analyze_video(file_path: str):
    try:
        if not os.path.exists(file_path):
            return {"error": "File path not found on server"}

        print("Uploading file to Gemini...")
        video_file = client.files.upload(file=file_path)

        while getattr(video_file.state, 'name', video_file.state) == "PROCESSING":
            print("Gemini is processing the video... waiting 5 seconds...")
            time.sleep(5)
            video_file = client.files.get(name=video_file.name)

        if getattr(video_file.state, 'name', video_file.state) == "FAILED":
            return {"error": "Gemini video processing failed"}

        print("Analyzing video content...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                video_file,
                "Provide a detailed, chronological breakdown of this video. Format as timestamp blocks like: [MM:SS] - description. Do not add markdown headers."
            ]
        )

        analysis_text = response.text
        filename = os.path.basename(file_path)

        # 🧠 DATABASE STORAGE STEP
        # We split the text response into separate lines to store them individually
        lines = [line.strip() for line in analysis_text.split('\n') if line.strip()]
        
        for index, line in enumerate(lines):
            # Save each line as its own unique vector document entry
            collection.add(
                documents=[line],
                metadatas=[{"source": filename, "line_number": index}],
                ids=[f"{filename}_line_{index}"]
            )
            
        print(f"Successfully stored {len(lines)} video segments into ChromaDB memory!")

        return {
            "status": "success",
            "analysis": analysis_text,
            "saved_segments_count": len(lines)
        }
        
    except Exception as e:
        return {"error": str(e)}


# 🔍 BRAND NEW ENDPOINT: Search our stored memory!
@app.get("/search-video")
async def search_video(query: str):
    try:
        # Ask ChromaDB to find the top 3 lines that match the meaning of our query string
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        return {
            "query": query,
            "matches": results['documents'][0]
        }
    except Exception as e:
        return {"error": str(e)}