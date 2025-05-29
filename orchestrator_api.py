# orchestrator_api.py
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from orchestrator.orchestrator import finance_team
from dotenv import load_dotenv
load_dotenv()

app = FastAPIApp(team=finance_team).get_app()

# Mount voice routes
from fastapi_server.routes.endpoints import router as voice_router
app.include_router(voice_router)

if __name__ == "__main__":
    serve_fastapi_app("orchestrator_api:app", port=8001, reload=True)
