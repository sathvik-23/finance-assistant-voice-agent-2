import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.models.groq import GroqTools
from agno.utils.media import save_base64_data

# Load environment variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Set default values if not found in .env
transcription_model = os.getenv("GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3")
translation_model   = os.getenv("GROQ_TRANSLATION_MODEL", "whisper-large-v3")
tts_model           = os.getenv("GROQ_TTS_MODEL", "playai-tts")
tts_voice           = os.getenv("GROQ_TTS_VOICE", "Chip-PlayAI")

# Sanity check for Groq models
missing = []
if not transcription_model:
    missing.append("GROQ_TRANSCRIPTION_MODEL")
if not tts_model:
    missing.append("GROQ_TTS_MODEL")
if missing:
    raise ValueError(f"Missing required Groq config(s): {', '.join(missing)}")

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
            show_tool_calls=True,
        )

    def transcribe_audio(self, file_path: str) -> str:
        """Return transcript from audio file via GroqTools."""
        result = self.agent.run(f"Please transcribe the audio file at '{file_path}'")
        return result.content if result else ""

    def speak_text(self, text: str, output_path: str) -> None:
        """Generate speech MP3 from text via GroqTools and save it."""
        result = self.agent.run(f"Convert this text to speech: {text}")
        if result and result.audio:
            save_base64_data(result.audio[0].base64_audio, output_path)
