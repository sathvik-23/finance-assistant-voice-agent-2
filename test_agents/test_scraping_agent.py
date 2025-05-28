from agents.scraping_agent.scraping_agent import scraping_agent

if __name__ == "__main__":
    prompt = "Scrape and summarize latest filings from Asia tech companies' IR websites."
    print(">>> Running Scraping Agent Test...")
    scraping_agent.print_response(prompt, stream=True)
