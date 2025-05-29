# agents/analysis_agent/analysis_agent.py

from agno.agent import Agent
from agno.models.google import Gemini

analysis_agent = Agent(
    name="analysis-agent",
    model=Gemini(id="gemini-1.5-flash"),  # fixed model ID
    read_chat_history=True,
    show_tool_calls=False,
    search_knowledge=False,
    markdown=True,
    instructions=[
        "You are a financial analysis agent.",
        "Based on the data from API and Scraping agents, return structured JSON insights.",
        "Your output should have the following keys: 'aum_allocation', 'earnings_surprises', and 'sentiment'.",
        "Example output: { 'aum_allocation': { 'asia_tech_percent_today': 22, 'asia_tech_percent_yesterday': 18 }, 'earnings_surprises': [ { 'company': 'TSMC', 'beat_estimates_by_percent': 4 }, { 'company': 'Samsung', 'missed_estimates_by_percent': 2 } ], 'sentiment': 'neutral with a cautionary tilt due to rising yields' }",
        "Do NOT write a summary — return only the structured JSON object."
    ]
)
