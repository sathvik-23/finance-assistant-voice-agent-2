from agno.agent import Agent
from agno.models.google import Gemini

# Analysis Agent – synthesizes retrieved and scraped data into insights
analysis_agent = Agent(
    name="analysis-agent",
    model=Gemini(id="models/gemini-1.5-flash"),
    read_chat_history=True,  # this allows it to use responses from other agents
    show_tool_calls=False,
    search_knowledge=False,  # it's not a retriever itself
    markdown=True,
)
