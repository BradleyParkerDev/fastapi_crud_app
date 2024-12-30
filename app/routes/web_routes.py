from fastapi import APIRouter, Request, Response
from app.controllers.web import home_page_controller

class WebRoutes():

    # Class constructor
    def __init__(self):
        self.router = APIRouter()

    # Individual Routes
    def setup_routes(self):
        @self.router.get("/")
        async def home_page_route(request:Request, response:Response):
            return await home_page_controller(request, response)

        return self.router
    
