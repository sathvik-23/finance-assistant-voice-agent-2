import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pineconedb import PineconeDb
from agno.embedder.google import GeminiEmbedder


# 1️⃣ Load .env variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# force Gemini to produce 512-dimension embeddings
embedder = GeminiEmbedder(dimensions=512)


# 2️⃣ Pinecone Vector DB (512-dim for Gemini)
vector_db = PineconeDb(
    name=PINECONE_INDEX_NAME,
    dimension=512,  # must match the index dimension
    metric="euclidean",
    api_key=PINECONE_API_KEY,
    spec={"serverless": {"cloud": "aws", "region": PINECONE_ENVIRONMENT}},
    embedder=embedder,  # 👈 critical fix
)


# 3️⃣ Create PDF knowledge base (from folder)
knowledge_base = PDFKnowledgeBase(
    path="/Users/sathvik/Documents/finance-assistant-voice-agent-2/data_ingestion/data/Financial_Summary.pdf",                          # 📁 folder containing PDFs
    vector_db=vector_db,
    reader=PDFReader(chunk=True),             # ✅ enables chunked reading
)

# 4️⃣ Load into Pinecone
knowledge_base.load(recreate=False, upsert=True)

# 5️⃣ Define agent
retriever_agent = Agent(
    name="retriever-agent",
    model=Gemini(id="gemini-2.0-flash"),
    knowledge=knowledge_base,
    search_knowledge=True,
    show_tool_calls=True,
    read_chat_history=True,
)
