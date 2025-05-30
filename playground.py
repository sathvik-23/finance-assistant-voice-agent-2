from agno.playground import Playground, serve_playground_app
from orchestrator.orchestrator import finance_team

app = Playground(
    teams=[
        finance_team,
    ]
).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", port=7777, reload=True)