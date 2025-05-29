# orchestrator_api.py

from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from orchestrator.orchestrator import finance_team

# Wrap your orchestrator team as a FastAPI app
app = FastAPIApp(team=finance_team).get_app()

if __name__ == "__main__":
    serve_fastapi_app("orchestrator_api:app", port=8001, reload=True)
