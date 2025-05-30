import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_server.routes.endpoints import router as voice_router
from orchestrator.orchestrator import finance_team
from agno.app.fastapi.app import FastAPIApp

# 1️⃣ Load local .env for development (Render/Heroku will inject env vars)
load_dotenv()

# 2️⃣ Wrap your FinanceOrchestratorTeam in a FastAPI app
app: FastAPI = FastAPIApp(team=finance_team).get_app()

# 3️⃣ Mount your /voice endpoints alongside /v1/run
app.include_router(voice_router)

# 4️⃣ Allow CORS from anywhere (or lock down to your front end’s domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5️⃣ If you need a manual file-size guard before Uvicorn’s limit:
@app.middleware("http")
async def limit_upload_size(request, call_next):
    max_bytes = 100 * 1024 * 1024  # 100 MB
    cl = request.headers.get("content-length")
    if cl and int(cl) > max_bytes:
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "Request too large"}, status_code=413)
    return await call_next(request)

# 6️⃣ Entrypoint for `python orchestrator_api.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "orchestrator_api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
        # 🚨 bump Uvicorn’s own body limit (default ~16 MB) to 100 MB
        limit_max_request_size=100_000_000,
    )
