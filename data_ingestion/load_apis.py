import os
from dotenv import load_dotenv
from agno.knowledge.pdf_file import PDFFileKnowledgeBase
from agno.vectordb.pineconedb import PineconeDb
from agno.embedder.google import GeminiEmbedder

# 1️⃣ Load credentials
load_dotenv()
PINECONE_API_KEY    = os.getenv("PINECONE_API_KEY")
PINECONE_ENV        = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# 2️⃣ Define embedder
embedder = GeminiEmbedder(dimensions=512)  # Optional: pass API key if needed

# 3️⃣ Define Pinecone Vector DB with hybrid search
vector_db = PineconeDb(
    name=PINECONE_INDEX_NAME,
    dimension=512,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": PINECONE_ENV}},
    api_key=PINECONE_API_KEY,
    use_hybrid_search=True,
    hybrid_alpha=0.5,
    embedder=embedder,
)

# 4️⃣ List local PDF files
pdf_paths = [
    "data_ingestion/data/Financial_Summary_Adobe.pdf",
    "data_ingestion/data/Financial_Summary_Nvidia.pdf",
    # Add more here...
]

# 5️⃣ Upload documents
for path in pdf_paths:
    if not os.path.exists(path):
        print(f"❌ Skipping missing file: {path}")
        continue

    knowledge_base = PDFFileKnowledgeBase(
        files=[path],
        vector_db=vector_db
    )

    print(f"📚 Uploading: {path}")
    knowledge_base.load(recreate=False, upsert=True)

print("✅ All PDFs processed and embedded.")
