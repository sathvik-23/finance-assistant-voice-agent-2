import streamlit as st
import requests, base64
from datetime import datetime

st.set_page_config(page_title="Finance Assistant", layout="centered")
st.title("🎙️ Voice & Text Multi-Agent Finance Assistant")

VOICE_API_TRANSCRIBE = "http://localhost:8001/voice/transcribe"
ORCHESTRATOR_API     = "http://localhost:8001/v1/run"
VOICE_API_SPEAK      = "http://localhost:8001/voice/speak"

# ─────────────────────────────────────────────
# 1️⃣ Type your question (Text Input)
# ─────────────────────────────────────────────
st.markdown("## 1️⃣ Type a question (fallback)")
user_q = st.text_input("Your question")

if st.button("▶️ Submit Text") and user_q:
    with st.spinner("🤖 Agents are analyzing your question…"):
        resp = requests.post(
            ORCHESTRATOR_API,
            data={
                "message": user_q,
                "stream": "false",
                "session_id": f"text-{datetime.now().isoformat()}"
            }
        )
    if resp.status_code != 200:
        st.error(f"❌ API Error: {resp.status_code}\n{resp.text}")
    else:
        data = resp.json()
        st.markdown("### 🧠 Final Summary")
        st.markdown(data.get("content", "*No summary returned.*"))

        for i, call in enumerate(data.get("tool_calls", []), 1):
            st.markdown(f"### 🛠️ Tool Call {i}")
            st.code(call.get("raw", str(call)))

        for resp in data.get("member_responses", []):
            with st.expander(resp.get("agent", {}).get("name", "Agent")):
                st.markdown(resp.get("content", ""))

# ─────────────────────────────────────────────
# 2️⃣ Speak your question (Voice File Upload)
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 2️⃣ Or speak your question")

uploaded = st.file_uploader("🎤 Upload a voice file (WAV or MP3)", type=["wav", "mp3"])

if uploaded:
    audio_bytes = uploaded.read()
    st.success(f"✅ Audio uploaded: {uploaded.name} ({len(audio_bytes)} bytes)")
    st.audio(audio_bytes, format="audio/wav")

    if st.button("✅ Submit Voice"):
        with st.spinner("🔁 Transcribing and sending to agents..."):
            try:
                # 1. Transcribe via STT
                r1 = requests.post(
                    VOICE_API_TRANSCRIBE,
                    files={"audio_file": (uploaded.name, audio_bytes, uploaded.type)}
                )
                r1.raise_for_status()
                transcript = r1.json().get("transcript", "")

                # 2. Send transcript to orchestrator
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

        # ─ Display Results ─
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

        # Optional: TTS
        if st.button("🔊 Speak Summary"):
            r3 = requests.post(VOICE_API_SPEAK, data={"text": data.get("content", "")})
            if r3.status_code == 200:
                st.audio(base64.b64decode(r3.json().get("audio", "")), format="audio/mp3")
            else:
                st.error("❌ TTS failed.")
