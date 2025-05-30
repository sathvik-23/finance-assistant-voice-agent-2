import os
import io
import base64
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.models.groq import GroqTools

load_dotenv()

class VoiceAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.agent = Agent(
            name="Voice Agent Utility",
            model=Gemini(id="gemini-1.5-flash", api_key=api_key),
            tools=[GroqTools(
                transcription_model=os.getenv("GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3"),
                translation_model=os.getenv("GROQ_TRANSLATION_MODEL", "whisper-large-v3"),
                tts_model=os.getenv("GROQ_TTS_MODEL", "playai-tts"),
                tts_voice=os.getenv("GROQ_TTS_VOICE", "Chip-PlayAI")
            )],
            show_tool_calls=False,
        )

    def transcribe_audio(self, file_path: str) -> str:
        result = self.agent.run(f"Please transcribe the audio file at '{file_path}'")
        return result.content if result else ""

    def speak_text_to_buffer(self, text: str, buffer: io.BytesIO) -> None:
        result = self.agent.run(f"Convert this text to speech: {text}")
        if not result or not result.audio:
            raise RuntimeError("TTS generation failed")
        audio_bytes = base64.b64decode(result.audio[0].base64_audio)
        buffer.write(audio_bytes)
        buffer.seek(0)

    def speak_text(self, text: str, file_path: str) -> None:
        result = self.agent.run(f"Convert this text to speech: {text}")
        if not result or not result.audio:
            raise RuntimeError("TTS generation failed")
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(result.audio[0].base64_audio))
