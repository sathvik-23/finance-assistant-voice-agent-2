# fastapi_server/routes/endpoints.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import io
import base64

from agents.voice_agent.voice_agent import VoiceAgent  # ⬅️ This is your utility class

voice_agent = VoiceAgent()
router = APIRouter()

@router.post("/voice/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Save audio to a temporary file
        temp_path = "/tmp/temp_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(await audio_file.read())

        transcript = voice_agent.transcribe_audio(temp_path)
        return JSONResponse({"transcript": transcript})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/voice/speak")
async def speak_text(text: str = Form(...)):
    try:
        mp3_buffer = io.BytesIO()
        voice_agent.speak_text_to_buffer(text, mp3_buffer)
        size = mp3_buffer.getbuffer().nbytes
        print(f"✅ TTS buffer size: {size} bytes")
        if size == 0:
            raise RuntimeError("TTS buffer is empty!")

        audio_b64 = base64.b64encode(mp3_buffer.getvalue()).decode()
        return JSONResponse({"audio": audio_b64})
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})