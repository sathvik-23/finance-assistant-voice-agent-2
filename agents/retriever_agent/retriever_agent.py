import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pineconedb import PineconeDb
from agno.embedder.google import GeminiEmbedder

# 1️⃣ Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# 2️⃣ Gemini Embedder (512-dim)
embedder = GeminiEmbedder(dimensions=512)

# 3️⃣ Pinecone Vector DB
vector_db = PineconeDb(
    name=PINECONE_INDEX_NAME,
    dimension=512,
    metric="euclidean",
    api_key=PINECONE_API_KEY,
    spec={"serverless": {"cloud": "aws", "region": PINECONE_ENVIRONMENT}},
    embedder=embedder,
)

# 4️⃣ PDF Knowledge Base
knowledge_base = PDFKnowledgeBase(
    path="/Users/sathvik/Documents/finance-assistant-voice-agent-2/data_ingestion/data/Financial_Summary.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

# 5️⃣ Load (disable re-embedding)
try:
    print("ℹ️ Loading knowledge base...")
    knowledge_base.load(recreate=False, upsert=False)
    print("✅ Knowledge base loaded without re-embedding.")
except Exception as e:
    print(f"⚠️ Skipped embedding. Reason: {e}")

# 6️⃣ Define Agent
retriever_agent = Agent(
    name="retriever-agent",
    model=Gemini(id="gemini-2.0-flash"),
    knowledge=knowledge_base,
    search_knowledge=True,
    show_tool_calls=True,
    read_chat_history=True,
)
