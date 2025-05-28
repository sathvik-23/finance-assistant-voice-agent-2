import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from textwrap import dedent

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")  # 👈 match orchestrator’s expectation

# Define the API Agent
api_agent = Agent(
    name="API Agent",
    role="Fetches market data from Yahoo Finance",
    model=Gemini(
        id="gemini-2.0-flash",
        api_key=api_key,
        search=True
    ),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=dedent("""\
        You are a market data-fetching agent responsible for compiling raw, structured information that will be passed to a language agent for verbal summarization.

        === TASK ===
        Collect and return structured data related to:
        1. Portfolio allocation to Asia tech sector
        2. Earnings surprises for major Asia tech companies
        3. Regional market sentiment

        === REQUIRED OUTPUT FORMAT ===
        {
            "aum_exposure_today": "22%",
            "aum_exposure_yesterday": "18%",
            "earnings_surprises": [
                { "company": "TSMC", "result": "beat", "percentage": 4 },
                { "company": "Samsung", "result": "missed", "percentage": -2 }
            ],
            "regional_sentiment": "neutral with a cautionary tilt due to rising yields"
        }

        === DATA GATHERING STEPS ===

        1. **Exposure**
           - Estimate allocation to Asia tech stocks (simulated or from `portfolio` if available).
           - If unavailable, return placeholders with a `"source": "manual override"` flag.

        2. **Earnings**
           - For each: TSMC, Samsung, MediaTek, Sony, Alibaba, Tencent:
             • Compare actual EPS to estimate
             • If EPS is missing or stale, exclude the company

        3. **Sentiment**
           - Analyze latest market news for Asia
           - Use index trend data (e.g., Nikkei 225, Hang Seng, KOSPI)
           - Check for macro indicators like yield or inflation moves

        === CONSTRAINTS ===
        - All output must be in JSON
        - No narration or summary
        - Do not hallucinate numbers: return null or note `"source": "not available"` if needed

        Your job ends once you've produced structured, accurate raw data.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Test locally
if __name__ == "__main__":
    api_agent.print_response(
        "What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?",
        stream=True
    )
