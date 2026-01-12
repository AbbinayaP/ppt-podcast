import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.ppt_extractor import extract_text_from_ppt
from services.llm_generator import generate_podcast_script
from services.tts_generator import generate_audio


# ================== APP INIT ==================
app = FastAPI(title="PPT Podcaster API")


# ================== CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== PATHS (ABSOLUTE – FIXES WINDOWS ISSUE) ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(STATIC_DIR, exist_ok=True)


# ================== STATIC FILES ==================
# Audio files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Frontend CSS & JS (FIXED)
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


# ================== FRONTEND ROUTE ==================
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ================== RESPONSE MODEL ==================
class ProcessResponse(BaseModel):
    script: str
    audio_url: str


# ================== HEALTH CHECK ==================
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ================== UPLOAD ENDPOINT ==================
@app.post("/upload", response_model=ProcessResponse)
async def upload_ppt(file: UploadFile = File(...)):

    if not file.filename.endswith((".pptx", ".ppt")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PPT or PPTX file."
        )

    file_id = str(uuid.uuid4())
    ppt_path = os.path.join(STATIC_DIR, f"{file_id}_{file.filename}")

    try:
        # Save PPT
        with open(ppt_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        ppt_text = extract_text_from_ppt(ppt_path)
        if not ppt_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PPT."
            )

        # Generate script
        script = generate_podcast_script(ppt_text)

        # Generate audio
        audio_filename = f"{file_id}.mp3"
        audio_path = os.path.join(STATIC_DIR, audio_filename)
        await generate_audio(script, audio_path)

        audio_url = f"http://127.0.0.1:8000/static/{audio_filename}"

        return ProcessResponse(script=script, audio_url=audio_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(ppt_path):
            os.remove(ppt_path)
# ================== RUN APP ==================
