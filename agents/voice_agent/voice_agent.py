import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.models.groq import GroqTools
from agno.utils.media import save_base64_data

# Load environment variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
transcription_model = os.getenv("GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3")
translation_model   = os.getenv("GROQ_TRANSLATION_MODEL", "whisper-large-v3")
tts_model           = os.getenv("GROQ_TTS_MODEL", "playai-tts")
tts_voice           = os.getenv("GROQ_TTS_VOICE", "Chip-PlayAI")

# Sanity check
if not google_api_key:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")

class VoiceAgent:
    def __init__(self):
        self.agent = Agent(
            name="Voice Agent",
            model=Gemini(id="gemini-1.5-flash", api_key=google_api_key),
            tools=[GroqTools(
                transcription_model=transcription_model,
                translation_model=translation_model,
                tts_model=tts_model,
                tts_voice=tts_voice
            )],
            show_tool_calls=False,
        )

    def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio using Groq STT"""
        result = self.agent.run(f"Please transcribe the audio file at '{file_path}'")
        return result.content if result else ""

    def speak_text(self, text: str, output_path: str) -> None:
        """Generate audio from text using Groq TTS and save as MP3"""
        result = self.agent.run(f"Convert this text to speech: {text}")
        if not result or not result.audio:
            raise RuntimeError("TTS generation failed")
        save_base64_data(result.audio[0].base64_audio, output_path)
