import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Safely load the API Key from Environment Variables
# This works because you added GEMINI_API_KEY to your Render Dashboard
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set!")

# Configure the Google Gemini Client
genai.configure(api_key=api_key)

@app.get("/")
def read_root():
    return {"message": "Smart Video Analyzer Backend is Live!"}

# --- Add your video processing routes here ---
# Example route to test connection:
@app.get("/test-gemini")
def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello, Gemini!")
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}