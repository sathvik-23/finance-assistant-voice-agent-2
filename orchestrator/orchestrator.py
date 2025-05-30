import os
from dotenv import load_dotenv
from agno.models.google import Gemini
from agno.team import Team
from agno.agent import Agent
from agno.tools.models.groq import GroqTools

# 1️⃣ Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# 2️⃣ Import all agent instances
from agents.api_agent.api_agent import api_agent
from agents.scraping_agent.scraping_agent import scraping_agent
from agents.retriever_agent.retriever_agent import retriever_agent
from agents.analysis_agent.analysis_agent import analysis_agent
from agents.language_agent.language_agent import language_agent

# 3️⃣ Define shared Gemini model
gemini_model = Gemini(id="gemini-1.5-flash", api_key=api_key)

# 4️⃣ Voice Agent (GroqTools for transcription + TTS)
transcription_model = os.getenv("GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3")
translation_model   = os.getenv("GROQ_TRANSLATION_MODEL", "whisper-large-v3")
tts_model           = os.getenv("GROQ_TTS_MODEL", "playai-tts")
tts_voice           = os.getenv("GROQ_TTS_VOICE", "Chip-PlayAI")

voice_agent_agent = Agent(
    name="Voice Agent",
    model=gemini_model,
    tools=[
        GroqTools(
            transcription_model=transcription_model,
            translation_model=translation_model,
            tts_model=tts_model,
            tts_voice=tts_voice,
        )
    ],
    description="Handles transcription of audio and generation of text-to-speech output using Groq tools.",
    debug_mode=True,
    show_tool_calls=True,
)

# 5️⃣ Define the orchestrator team
finance_team = Team(
    name="FinanceOrchestratorTeam",
    mode="coordinate",  # agent-by-agent tasking
    model=gemini_model,
    members=[
        api_agent,
        scraping_agent,
        retriever_agent,
        analysis_agent,
        language_agent,
        voice_agent_agent,  # ✅ Voice Agent added to team
    ],
    description="Coordinates agents to gather financial data, analyze, and present polished summaries.",
    instructions=[
        "Start by asking the API Agent to fetch financial and market metrics.",
        "Then ask the Scraping Agent to get press releases or investor updates.",
        "Then ask the Retriever Agent to pull internal PDF knowledge if relevant.",
        "Then ask the Analysis Agent to output structured insights in JSON format with keys: aum_allocation, earnings_surprises, and sentiment.",
        "Then ask the Language Agent to use the `generate_market_brief` tool with the insights JSON to produce a spoken-style response.",
        "Finally, ask the Voice Agent to convert the spoken-style response to audio using text-to-speech.",
    ],
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
    debug_mode=True,
    show_tool_calls=True,
)

# 6️⃣ Optional test run
if __name__ == "__main__":
    prompt = "Summarize Nvidia’s Q1 2025 earnings."
    print(">>> Running Finance Orchestrator...")
    finance_team.print_response(prompt, stream=True)
