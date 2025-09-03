import os
import asyncio
import uvicorn
# from agno.app.agui.app import AGUIApp  # <-- Uncomment this to test the bug
from lib.app.agui.app import AGUIApp     # <-- Uncomment this to test the fix
from contextlib import asynccontextmanager
from fastapi import FastAPI

from telemetry import start_telemetry
from agents.investment_advisor_team import investment_advisor_team
# from agents.investment_advisor_workflow import stock_research_workflow

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # Application runs after this yield

async def main():
    start_telemetry()

    # await stock_research_workflow.aprint_response("Tesla")
    # return

    agui_app = AGUIApp(
        # workflow=stock_research_workflow,
        team=investment_advisor_team,
        # agent=stock_price_agent,
        name="multiagent_agui",
        app_id="multiagent_agui",
        description="Multiagent AGUI",
    )

    app = agui_app.get_app()
    app.router.lifespan_context = lifespan

    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())

