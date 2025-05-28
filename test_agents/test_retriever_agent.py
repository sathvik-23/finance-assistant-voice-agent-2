import sys
import os

# Add project root to sys.path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.retriever_agent.retriever_agent import retriever_agent

if __name__ == "__main__":
    query = "What does Adobe's financial summary say?"
    print(">>> Running Retriever Agent Test...\n")
    retriever_agent.print_response(query, stream=True)
