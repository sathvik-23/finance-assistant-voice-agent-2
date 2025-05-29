# fastapi_server/routes/endpoints.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile, base64
from agents.voice_agent import voice_agent

router = APIRouter()

@router.post("/voice/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Save upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio_file.read())
            path = tmp.name
        # STT
        transcript = voice_agent.transcribe_audio(path)
        # TTS
        out_mp3 = path.replace(".wav", ".mp3")
        voice_agent.speak_text(transcript, out_mp3)
        # Return base64 MP3
        with open(out_mp3, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
        return JSONResponse({"transcript": transcript, "audio": audio_b64})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/voice/speak")
async def speak_text(text: str = Form(...)):
    try:
        # TTS only
        out_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        voice_agent.speak_text(text, out_mp3)
        with open(out_mp3, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
        return JSONResponse({"audio": audio_b64})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
