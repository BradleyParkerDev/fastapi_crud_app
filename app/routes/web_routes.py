from fastapi import APIRouter, Request, Response
from app.controllers import home_page_controller



class WebRoutes:
    def __init__(self):
        self.router = APIRouter()
        
    def setup_routes(self):
        @self.router.get('/')
        async def home_page_route(request:Request, response:Response):
            return await home_page_controller(request,response)
        
        # Ensure the router is returned here
        return self.router