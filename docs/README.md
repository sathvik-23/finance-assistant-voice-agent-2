# 🧠 Multi-Agent Financial Assistant (Voice + Text)

This is a modular, multi-agent financial assistant that generates real-time market insights and spoken briefings using coordinated AI agents. Built with [Agno](https://github.com/agnos-ai/agno), Streamlit, and FastAPI.

---

## 🎯 Use Case: Morning Market Brief

> “What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?”

📢 The assistant responds:

> “Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields.”

---

## 🏗️ Architecture Overview

- **Agno Framework** – Modular agent orchestration and memory.
- **Streamlit App** – Frontend for chat + real-time summaries.
- **FastAPI Server** – Hosts agent team as a REST API.
- **LangGraph-style Coordination** – Sequential agent reasoning.
- **Gemini API (Google)** – Used for LLM and embedding logic.
- **Optional** – PDF parsing, web scraping, Pinecone vector retrieval.

---

## 🧠 Agent Roles

| Agent             | Purpose                                                       |
| ----------------- | ------------------------------------------------------------- |
| `api-agent`       | Pulls real-time metrics via Yahoo/AlphaVantage                |
| `scraping-agent`  | Extracts news/filings from investor portals                   |
| `retriever-agent` | Retrieves embedded documents from Pinecone                    |
| `analysis-agent`  | Synthesizes structured market insights                        |
| `language-agent`  | Calls `generate_market_brief()` to craft spoken-style summary |

---

## 🗃️ Project Structure

```
.
├── agents/                    # Modular agents (API, scraping, etc.)
├── orchestrator/             # Main coordinator (Agno Team)
├── streamlit_app/            # Frontend interface
├── fastapi_server/           # FastAPI wrapper for agent team
├── data_ingestion/           # Document loaders, scrapers
├── requirements.txt
├── orchestrator_api.py       # FastAPI app entrypoint
├── run.sh
└── docs/
    ├── README.md             # You're here!
    ├── ai_tool_usage.md      # Prompt/code generation audit
    └── architecture.png      # Visual diagram
```

---

## 🚀 Running the App

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/finance-assistant.git
cd finance-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=...
PINECONE_INDEX_NAME=...
```

### 3. Start the Orchestrator (FastAPI)

```bash
python orchestrator_api.py
```

Runs at: [http://localhost:8001/docs](http://localhost:8001/docs)

### 4. Start the Streamlit App

```bash
streamlit run streamlit_app/main.py
```

Runs at: [http://localhost:8501](http://localhost:8501)

---

## 🔄 How It Works

1. **User** enters a market question in Streamlit.
2. **FastAPI server** receives the query and streams the response.
3. **Agno team** coordinates each agent:
   - Fetches data
   - Scrapes news
   - Analyzes risks
   - Synthesizes summary
4. **Streamlit** shows per-agent steps + final polished response.

---

## 📦 Tooling

- 🧠 **Agno**: agent orchestration
- 🗂️ **Pinecone**: vector DB for documents (optional)
- 📢 **Google Gemini API**: LLM + embeddings
- 🎨 **Streamlit**: frontend UI
- 🚀 **FastAPI**: backend orchestration API
- 📜 **Whisper / Coqui / Piper**: for STT/TTS (optional voice mode)

---

## 📊 Screenshots

> Add visuals showing:

- Streamlit app in action
- Real-time agent progress
- Final spoken-style summaries

---

## 📄 Documentation

- [`docs/ai_tool_usage.md`](./docs/ai_tool_usage.md): Logs of AI-generated prompts & code.
- [`docs/architecture.png`](./docs/architecture.png): Agent architecture flow.

---

## 🧪 Tests

Run unit tests for agent behaviors:

```bash
pytest test_agents/
```

---

## 📦 Deployment

You can deploy:

- 🚢 FastAPI backend via Render/Fly.io
- 🛰️ Streamlit app on [Streamlit Cloud](https://streamlit.io/cloud)

---

## ✅ To Do

- [ ] Add STT/TTS voice agent (Whisper + Piper)
- [ ] Dockerize + add `docker-compose.yml`
- [ ] Deploy backend + frontend live

---

## 🙌 Credits

Built with:

- [Agno Framework](https://github.com/agnos-ai/agno)
- [Streamlit](https://streamlit.io)
- [Google Gemini](https://ai.google.dev)
- [Pinecone](https://www.pinecone.io)

---

## 🛡️ Disclaimer

This system is for **educational use only** and not intended as financial advice. Always consult a qualified professional before making investment decisions.
