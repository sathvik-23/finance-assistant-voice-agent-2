# import os
# from dotenv import load_dotenv
# load_dotenv()
# from orchestrator.orchestrator import finance_team
# from agno.app.fastapi.app import FastAPIApp

# from agno.app.fastapi.serve import serve_fastapi_app


# # Async router by default (use_async=True)
# app = FastAPIApp(team=finance_team).get_app()


# if __name__ == "__main__":
#     # Assumes script is `basic_app.py`; update if different.
#     serve_fastapi_app("api:app", port=8001, reload=True)


# api.py
import os
from dotenv import load_dotenv
load_dotenv()

from orchestrator.orchestrator import finance_team
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app

from fastapi_server.routes import endpoints  # ✅ ADD THIS

# Create app with team
app = FastAPIApp(team=finance_team).get_app()

# ✅ Include voice routes
app.include_router(endpoints.router)

if __name__ == "__main__":
    serve_fastapi_app("api:app", port=8001, reload=True)
