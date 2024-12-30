from arel import HotReload, Path
from starlette.routing import WebSocketRoute
from contextlib import asynccontextmanager
from fastapi import FastAPI

class LayoutArelHelper():

    def __init__(self):
        # Initialize hot reload watching resources and public directories
        self.hotreload = HotReload(
            paths=[
                Path("resources", on_reload=[self.reload_data]),
                Path("public")
            ]
        )

    # Define the lifespan context manager
    @asynccontextmanager
    async def lifespan(self, app:FastAPI):
        await self.hotreload.startup()
        yield
        await self.hotreload.shutdown()

    # Hot reload callback
    async def reload_data(self):
        print("Reloading server data...")