# import os
# from dotenv import load_dotenv
# from agno.models.google import Gemini
# from agno.team import Team
# from agents.api_agent import api_agent
# from agents.scraping_agent import scraping_agent




# # Load env variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Load agents from their modules
# from agents.api_agent import api_agent
# from agents.scraping_agent import scraping_agent
# from agents.retriever_agent import retriever_agent
# from agents.analysis_agent import analysis_agent
# from agents.language_agent import language_agent

# # Define the shared model
# gemini_model = Gemini(
#     id="gemini-2.0-pro",  # or "gemini-2.0-flash"
#     api_key=GEMINI_API_KEY
# )

# # Create a coordinating Team that calls agents in sequence
# finance_team = Team(
#     name="FinanceBriefTeam",
#     mode="sequential",  # Executes agents one after the other
#     model=gemini_model,
#     members=[
#         api_agent,
#         scraping_agent,
#         retriever_agent,
#         analysis_agent,
#         language_agent
#     ],
#     description="This team generates a spoken finance market brief using multiple specialized agents.",
#     instructions=[
#         "1. API Agent should fetch latest market data (AUM, stock moves).",
#         "2. Scraping Agent should extract fresh filings.",
#         "3. Retriever Agent should return relevant chunks from document DB.",
#         "4. Analysis Agent must quantify exposure, sentiment, surprises.",
#         "5. Language Agent should synthesize all into a coherent market brief.",
#         "Respond clearly and with high confidence. If unsure, mention gaps.",
#     ],
#     add_datetime_to_instructions=True,
#     share_member_interactions=True,
#     enable_agentic_context=True,
#     show_members_responses=True,
#     markdown=True
# )

# # Example usage
# if __name__ == "__main__":
#     user_query = "What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"
#     finance_team.print_response(user_query)

import os
from dotenv import load_dotenv
from agno.models.google import Gemini
from agno.team import Team

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Import agent instances
from agents.api_agent.api_agent import api_agent
from agents.scraping_agent.scraping_agent import scraping_agent
from agents.retriever_agent.retriever_agent import retriever_agent


# Define shared model
gemini_model = Gemini(id="gemini-2.0-flash", api_key=api_key)

# Define coordinated Team
finance_team = Team(
    name="FinanceOrchestratorTeam",
    mode="coordinate",  # or "sequential"
    model=gemini_model,
    members=[api_agent, scraping_agent],
    description="Coordinates API and scraping agents to produce raw market data and disclosures.",
    instructions=[
        "First, the API Agent fetches market exposure and earnings data.",
        "Then, the Scraping Agent gathers relevant regulatory filings or press updates from IR websites.",
        "Return structured raw output from each agent for downstream processing.",
    ],
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
)

# Entry point
if __name__ == "__main__":
    prompt = "What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"
    print(">>> Running Orchestrator Team...")
    finance_team.print_response(prompt, stream=True)
