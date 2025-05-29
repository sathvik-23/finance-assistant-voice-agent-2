import base64
from io import BytesIO
from datetime import datetime
import requests
import streamlit as st
from audiorecorder import audiorecorder

# Streamlit setup
st.set_page_config(page_title="Finance Assistant", layout="centered")
st.title("🎙️ Voice & Text Multi-Agent Finance Assistant")

VOICE_API_TRANSCRIBE = "http://localhost:8001/voice/transcribe"
ORCHESTRATOR_API     = "http://localhost:8001/v1/run"
VOICE_API_SPEAK      = "http://localhost:8001/voice/speak"

# ── 1️⃣ TEXT INPUT ─────────────────────────────────────────────────────
st.markdown("## 1️⃣ Type a question (fallback)")
user_q = st.text_input("Your question")
if st.button("▶️ Submit Text") and user_q:
    with st.spinner("🤖 Agents are analyzing your question…"):
        try:
            resp = requests.post(ORCHESTRATOR_API, data={
                "message": user_q,
                "stream": "false",
                "session_id": f"text-{datetime.now().isoformat()}"
            })
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

    st.markdown("### 🧠 Final Summary")
    st.markdown(data.get("content", "*No summary returned.*"))

    for i, call in enumerate(data.get("tool_calls", []), 1):
        st.markdown(f"### 🛠️ Tool Call {i}")
        st.code(call.get("raw", str(call)))

    for resp in data.get("member_responses", []):
        with st.expander(resp.get("agent", {}).get("name", "Agent")):
            st.markdown(resp.get("content", ""))

# ── 2️⃣ VOICE INPUT ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 2️⃣ Speak or Upload your question")

# 🎤 Record voice
recorded_audio = audiorecorder("🎙️ Record", "⏹️ Stop", key="voice-rec")
recorded_bytes = None
if recorded_audio and hasattr(recorded_audio, "export"):
    buf = BytesIO()
    recorded_audio.export(buf, format="wav")
    recorded_bytes = buf.getvalue()

# 📁 Upload voice
uploaded_file = st.file_uploader("...or upload a .wav file", type=["wav"])
uploaded_bytes = uploaded_file.read() if uploaded_file else None

# 🎧 Playback & Status
final_audio = recorded_bytes or uploaded_bytes
if final_audio:
    st.success("✅ Audio ready!")
    st.audio(final_audio, format="audio/wav")

    if st.button("✅ Submit Voice"):
        with st.spinner("⏳ Transcribing and orchestrating..."):
            try:
                r1 = requests.post(
                    VOICE_API_TRANSCRIBE,
                    files={"audio_file": ("voice.wav", final_audio, "audio/wav")}
                )
                r1.raise_for_status()
                transcript = r1.json().get("transcript", "")

                r2 = requests.post(
                    ORCHESTRATOR_API,
                    data={
                        "message": transcript,
                        "stream": "false",
                        "session_id": f"voice-{datetime.now().isoformat()}"
                    }
                )
                r2.raise_for_status()
                data = r2.json()
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

        st.markdown("### 📝 Transcript")
        st.write(transcript or "*<no transcript>*")

        st.markdown("### 🧠 Final Summary")
        st.markdown(data.get("content", "*No summary returned.*"))

        for i, call in enumerate(data.get("tool_calls", []), 1):
            st.markdown(f"### 🛠️ Tool Call {i}")
            st.code(call.get("raw", str(call)))

        for resp in data.get("member_responses", []):
            with st.expander(resp.get("agent", {}).get("name", "Agent")):
                st.markdown(resp.get("content", ""))

        if st.button("🔊 Speak Summary"):
            r3 = requests.post(VOICE_API_SPEAK, data={"text": data.get("content", "")})
            if r3.status_code == 200:
                st.audio(base64.b64decode(r3.json().get("audio", "")), format="audio/mp3")
            else:
                st.error("TTS failed.")
