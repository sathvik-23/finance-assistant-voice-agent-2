from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import tool

@tool()
def generate_market_brief(insights: dict) -> str:
    """
    Generates a natural spoken-style financial summary from structured insights.
    Returns a string formatted for spoken delivery — e.g., "Today, Nvidia posted strong Q1..."
    """
    return f"""
You are a voice assistant for a finance executive.

Given the following structured insights, generate a professional, natural-sounding spoken briefing suitable for a portfolio manager.

Make it short (1–3 sentences), clear, and use natural language. Avoid bullet points or markdown.

Start with something like "Today" or "As of this morning".

Insights:
{insights}
"""

language_agent = Agent(
    name="language-agent",
    role="Formats structured financial insights into spoken market briefings",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[generate_market_brief],
    instructions=[
        "Your job is to call the `generate_market_brief` tool to receive a prompt and then generate the final natural language response.",
        "The response must be concise, clear, and suitable for voice delivery. No bullet points or markdown.",
        "Do not include tool call code in your output — return the final response only.",
    ],
    show_tool_calls=True,
    markdown=False,
)
