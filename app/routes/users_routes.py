from fastapi import APIRouter, Request, Response
from app.controllers.users import get_user_controller

class UsersRoutes():

    # Class constructor
    def __init__(self):
        self.router = APIRouter()

    # Individual Routes
    def setup_routes(self):
        @self.router.get("/api/users/get-user")
        async def get_user_route(request:Request, response:Response):
            return await get_user_controller(request, response)

        return self.router
    
