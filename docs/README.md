# 🧠 Multi-Agent Financial Assistant (Voice + Text)

This branch introduces and stabilizes voice capabilities for the AI-powered financial assistant, allowing users to interact through speech and receive audio responses using Groq's TTS models and Gemini orchestration.

---

## 🧠 Overview

The voice agent supports:

- 🎤 Transcription of audio to text
- 🌐 Translation (optional)
- 🗣️ Text-to-speech audio generation
- 🤖 Orchestrated multi-agent reasoning over financial data

---

## 🚀 Features

- **Voice-to-Text (STT)** via Groq Whisper
- **Text-to-Voice (TTS)** via Groq PlayAI
- **Streamlit UI** for seamless interaction
- **FastAPI backend** with orchestrated agents
- **Multi-agent coordination** using Gemini

---

## 🛠️ Setup Instructions

### 1. Clone and switch to this branch

```bash
git clone https://github.com/yourusername/finance-assistant-voice-agent.git
cd finance-assistant-voice-agent
git checkout chami
```

### 2. Setup virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the root:

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_TRANSCRIPTION_MODEL=whisper-large-v3
GROQ_TRANSLATION_MODEL=whisper-large-v3
GROQ_TTS_MODEL=playai-tts
GROQ_TTS_VOICE=Chip-PlayAI
```

---

## 🚦 Running the App

### ➤ Start FastAPI Backend

```bash
python api.py
```

Serves APIs on: `http://localhost:8001`

### ➤ Start Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

Access UI at: `http://localhost:8501`

---

## 🔊 API Endpoints

| Endpoint            | Method | Description                   |
| ------------------- | ------ | ----------------------------- |
| `/voice/transcribe` | POST   | Upload audio, return text     |
| `/voice/speak`      | POST   | Send text, return audio (b64) |
| `/v1/run`           | POST   | Run orchestrator team         |

---

## 🧩 Project Structure

```
├── agents/
│   └── voice_agent/
│       ├── voice_agent.py         # VoiceAgent class
│       └── voice_agent_agent.py   # Agent wrapper for orchestration
├── orchestrator/
│   └── orchestrator.py            # Team definition
├── fastapi_server/
│   └── routes/
│       └── endpoints.py           # /voice API handlers
├── streamlit_app.py               # Streamlit frontend
├── api.py                         # Backend entrypoint
├── .env                           # API keys
├── requirements.txt
└── README.md
```

---

## 🧪 Troubleshooting

- **500 error from /voice/speak**  
  → You’ve likely hit Groq’s daily TTS limit (token quota). Wait or upgrade tier.

- **Audio duration is 0 seconds**  
  → TTS failed silently or returned empty. Fallback logic recommended.

- **Transcription returns empty string**  
  → Ensure audio is in WAV/MP3 format and valid.

---

## 🤝 Contributing

```bash
git checkout -b feature/my-feature
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

Then open a pull request!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For questions, email [sathvik238@gmail.com]
