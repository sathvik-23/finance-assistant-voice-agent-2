# agents/language_agent/language_agent.py

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import tool

@tool()
def generate_market_brief(insights: dict) -> str:
    """
    Generates a natural spoken-style financial summary from structured insights.
    Returns a string formatted for spoken delivery — e.g., 
    "Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday..."
    """
    return f"""
You are a voice assistant for a finance executive.

Given the following structured insights, generate a professional, natural-sounding spoken briefing suitable for a portfolio manager.

Use a confident and concise tone.

Avoid markdown, bullet points, or long paragraphs. Keep it to 1–3 sentences.

Start with something like “Today” or “As of this morning”.

Insights:
{insights}
"""

language_agent = Agent(
    name="language-agent",
    role="Formats structured financial insights into spoken market briefings",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[generate_market_brief],
    instructions=[
        "Your job is to call the `generate_market_brief` tool.",
        "Pass the structured insights (from analysis-agent) to this tool as JSON.",
        "Return the final spoken-style response ONLY. No tool call code or explanation.",
        "The summary must sound like a brief verbal report to a finance executive.",
    ],
    show_tool_calls=True,
    markdown=False,
)
