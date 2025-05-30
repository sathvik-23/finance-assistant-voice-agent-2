import base64
from io import BytesIO
from datetime import datetime
import requests
import streamlit as st
from audio_recorder_streamlit import audio_recorder  # ✅ Streamlit Cloud–compatible

# Config
st.set_page_config(page_title="Finance Assistant", layout="centered")
st.title("🎙️ Voice & Text Multi-Agent Finance Assistant")

# API endpoints
VOICE_API_TRANSCRIBE = "https://finance-assistant-voice-agent-2.onrender.com/voice/transcribe"
VOICE_API_SPEAK = "https://finance-assistant-voice-agent-2.onrender.com/voice/speak"
ORCHESTRATOR_API = "https://finance-assistant-voice-agent-2.onrender.com/v1/run"

# ────────────── TEXT MODE ──────────────
st.markdown("## 1️⃣ Type a question")
text_input = st.text_input("Your question")
if st.button("▶️ Submit Text") and text_input:
    with st.spinner("🤖 Agents are analyzing your question..."):
        try:
            resp = requests.post(ORCHESTRATOR_API, data={
                "message": text_input,
                "stream": "false",
                "session_id": f"text-{datetime.now().isoformat()}"
            })
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

    content = result.get("content", "*No summary returned.*")
    parts = content.strip().split("\n")
    final_summary = parts[-1] if len(parts) > 1 else content

    st.markdown("### 🧠 Final Summary")
    st.markdown(final_summary)

    for i, call in enumerate(result.get("tool_calls", []), 1):
        st.markdown(f"### 🛠️ Tool Call {i}")
        st.code(call.get("raw", str(call)))

    for r in result.get("member_responses", []):
        with st.expander(r.get("agent", {}).get("name", "Agent")):
            st.markdown(r.get("content", ""))

    # 🔊 Speak Final Summary
    try:
        st.info("🔈 Speaking summary...")
        r3 = requests.post(VOICE_API_SPEAK, data={"text": final_summary})
        r3.raise_for_status()
        audio_base64 = r3.json().get("audio", "")
        if audio_base64:
            st.markdown("### 🔊 Audio Summary")
            st.audio(base64.b64decode(audio_base64), format="audio/mp3")
    except Exception as e:
        st.warning(f"⚠️ TTS failed: {e}")

# ────────────── VOICE MODE ──────────────
st.markdown("---")
st.markdown("## 2️⃣ Speak or Upload your question")

# 🎙️ Record (browser-safe)
recorded_audio = audio_recorder()

if recorded_audio:
    st.success("✅ Voice recorded!")
    st.audio(recorded_audio, format="audio/wav")

# 📁 Upload
uploaded_file = st.file_uploader("...or upload a .wav file", type=["wav"])
uploaded_bytes = uploaded_file.read() if uploaded_file else None

# Pick best available audio
final_audio = recorded_audio or uploaded_bytes

# ✅ Submit Voice
if final_audio:
    if st.button("✅ Submit Voice"):
        with st.spinner("⏳ Transcribing and orchestrating..."):
            try:
                r1 = requests.post(VOICE_API_TRANSCRIBE, files={
                    "audio_file": ("voice.wav", final_audio, "audio/wav")
                })
                r1.raise_for_status()
                transcript = r1.json().get("transcript", "")

                r2 = requests.post(ORCHESTRATOR_API, data={
                    "message": transcript,
                    "stream": "false",
                    "session_id": f"voice-{datetime.now().isoformat()}"
                })
                r2.raise_for_status()
                result = r2.json()
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

        st.markdown("### 📝 Transcript")
        st.write(transcript or "*No transcript returned.*")

        content = result.get("content", "*No summary returned.*")
        parts = content.strip().split("\n")
        final_summary = parts[-1] if len(parts) > 1 else content

        st.markdown("### 🧠 Final Summary")
        st.markdown(final_summary)

        for i, call in enumerate(result.get("tool_calls", []), 1):
            st.markdown(f"### 🛠️ Tool Call {i}")
            st.code(call.get("raw", str(call)))

        for r in result.get("member_responses", []):
            with st.expander(r.get("agent", {}).get("name", "Agent")):
                st.markdown(r.get("content", ""))

        # 🔊 Speak Final Summary
        try:
            st.info("🔈 Speaking summary...")
            r3 = requests.post(VOICE_API_SPEAK, data={"text": final_summary})
            r3.raise_for_status()
            audio_base64 = r3.json().get("audio", "")
            if audio_base64:
                st.markdown("### 🔊 Audio Summary")
                st.audio(base64.b64decode(audio_base64), format="audio/mp3")
        except Exception as e:
            st.warning(f"⚠️ TTS failed: {e}")
