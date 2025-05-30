# fastapi_server/routes/endpoints.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import base64, io
from agents.voice_agent import voice_agent

router = APIRouter()

@router.post("/voice/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Read audio in memory
        audio_bytes = await audio_file.read()
        transcript = voice_agent.transcribe_audio(audio_bytes)

        # Convert transcript to mp3 in memory
        mp3_buffer = io.BytesIO()
        voice_agent.speak_text(transcript, mp3_buffer)

        # Return base64 audio
        audio_b64 = base64.b64encode(mp3_buffer.getvalue()).decode()
        return JSONResponse({"transcript": transcript, "audio": audio_b64})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/voice/speak")
async def speak_text(text: str = Form(...)):
    try:
        mp3_buffer = io.BytesIO()
        voice_agent.speak_text(text, mp3_buffer)
        audio_b64 = base64.b64encode(mp3_buffer.getvalue()).decode()
        return JSONResponse({"audio": audio_b64})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
