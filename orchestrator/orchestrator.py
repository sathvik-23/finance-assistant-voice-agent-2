# orchestrator/orchestrator.py

import os
from dotenv import load_dotenv
from agno.models.google import Gemini
from agno.team import Team

# 1️⃣ Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2️⃣ Import all agent instances
from agents.api_agent.api_agent import api_agent
from agents.scraping_agent.scraping_agent import scraping_agent
from agents.retriever_agent.retriever_agent import retriever_agent
from agents.analysis_agent.analysis_agent import analysis_agent
from agents.language_agent.language_agent import language_agent

# 3️⃣ Define shared Gemini model
gemini_model = Gemini(id="gemini-1.5-flash", api_key=api_key)

# 4️⃣ Define orchestrator team using COORDINATE mode
finance_team = Team(
    name="FinanceOrchestratorTeam",
    mode="coordinate",  # ✅ Coordinate enables agent-by-agent tasking
    model=gemini_model,
    members=[
        api_agent,
        scraping_agent,
        retriever_agent,
        analysis_agent,
        language_agent,
    ],
    description="Coordinates agents to gather financial data, analyze, and present polished summaries.",
    instructions=[
        "Start by asking the API Agent to fetch financial and market metrics.",
        "Then ask the Scraping Agent to get press releases or investor updates.",
        "Then ask the Retriever Agent to pull internal PDF knowledge if relevant.",
        "Then ask the Analysis Agent to output structured insights in JSON format with keys: aum_allocation, earnings_surprises, and sentiment.",
        "Finally, the Language Agent must use the `generate_market_brief` tool with the insights JSON to produce a spoken-style response.",
    ],
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
    
)

# 5️⃣ Entry point
if __name__ == "__main__":
    prompt ="What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"
    print(">>> Running Finance Orchestrator...")
    finance_team.print_response(prompt, stream=True)


# "Summarize Nvidia’s Q1 2025 earnings?"