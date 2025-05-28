from agents.api_agent.api_agent import api_agent

if __name__ == "__main__":
    prompt = "What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"
    print(">>> Running API Agent Test...")
    api_agent.print_response(prompt, stream=True)
