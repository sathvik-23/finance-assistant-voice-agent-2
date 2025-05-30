from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_server.routes import endpoints  # assuming this is where your routes are defined

app = FastAPI(
    title="Finance Assistant Voice API",
    description="API for transcribing and speaking text",
    version="1.0.0"
)

# ✅ Enable CORS for Streamlit (especially for Streamlit Cloud or local port 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your existing endpoints
app.include_router(endpoints.router)
