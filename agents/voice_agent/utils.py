import base64
from pathlib import Path

def save_audio(base64_audio: str, output_path: Path):
    """
    Saves base64-encoded audio to a file.
    """
    audio_data = base64.b64decode(base64_audio)
    with open(output_path, "wb") as f:
        f.write(audio_data)
