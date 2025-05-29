from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.models.groq import GroqTools

# Initialize the voice agent
voice_agent = Agent(
    name="voice-agent",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[GroqTools()],
    instructions=[
        "You are a voice assistant that transcribes audio, understands queries, and provides spoken responses."
    ],
    show_tool_calls=True,
)
