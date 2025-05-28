import os
from dotenv import load_dotenv
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.website import WebsiteTools

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Define Scraping Agent using WebsiteTools
scraping_agent = Agent(
    name="Scraping Agent",
    role="Scrapes investor pages and IR websites to extract recent Asia tech disclosures",
    model=Gemini(
        id="gemini-2.0-flash",
        api_key=api_key
    ),
    tools=[WebsiteTools()],
    instructions=dedent("""\
        You are a web scraping agent for regulatory filings and company disclosures.

        === TASK ===
        For each of the following companies:
        - TSMC
        - Samsung
        - MediaTek
        - Sony
        - Alibaba
        - Tencent

        Visit their investor relations or filings websites and extract key updates (earnings, reports, press releases) from the last 7 days.

        === TOOL USAGE ===
        - Use `read_url` to read individual investor websites or press release pages.
        - Use `add_website_to_knowledge_base` if the full site should be stored for semantic retrieval.
        - Only use URLs that start with `https://`.

        === OUTPUT FORMAT ===
        Return a structured JSON array:
        [
            {
                "company": "Samsung",
                "title": "Q1 2025 Earnings Results",
                "date": "2025-05-27",
                "url": "https://.../investor/news/q1-2025",
                "summary": "Samsung posted a 2% miss on earnings with cautious forward guidance."
            },
            ...
        ]

        === CONSTRAINTS ===
        - Do not make up URLs or filings.
        - Only include companies with new updates in the past 7 days.
        - Ensure JSON format only — no narration or comments.
        - If no updates exist for a company, exclude them from the list.

        === NOTES ===
        Use publicly accessible investor relations pages or newsrooms from:
        - https://investor.tsmc.com
        - https://news.samsung.com
        - https://www.mediatek.com/investor-relations
        - https://www.sony.com/en/SonyInfo/IR
        - https://www.alibabagroup.com/en/news
        - https://www.tencent.com/en-us/investors.html

        Return only recent filings with clean summaries.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Run standalone
if __name__ == "__main__":
    scraping_agent.print_response(
        "Scrape and summarize latest filings from Asia tech companies' IR websites.",
        stream=True
    )
