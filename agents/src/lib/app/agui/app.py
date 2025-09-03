"""Main class for the AG-UI app, used to expose an Agno Agent or Team in an AG-UI compatible format."""

from fastapi.routing import APIRouter

from lib.app.agui.async_router import get_async_agui_router
from lib.app.agui.sync_router import get_sync_agui_router
from lib.app.base import BaseAPIApp


class AGUIApp(BaseAPIApp):
    type = "agui"

    def get_router(self) -> APIRouter:
        return get_sync_agui_router(agent=self.agent, team=self.team)

    def get_async_router(self) -> APIRouter:
        return get_async_agui_router(agent=self.agent, team=self.team, workflow=self.workflow)
