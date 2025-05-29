import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# # Retrieve the Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
### agents/voice_agent/config.py
GROQ_TRANSCRIPTION_MODEL = "whisper-large-v3"
GROQ_TRANSLATION_MODEL = "whisper-large-v3"
GROQ_TTS_MODEL = "playai-tts"
GROQ_TTS_VOICE = "Chip-PlayAI"
