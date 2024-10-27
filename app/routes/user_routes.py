from fastapi import APIRouter, Request, Response
from app.controllers import  register_user_controller, get_user_controller, update_user_controller, delete_user_controller

class UserRoutes:
    def __init__(self):
        self.router = APIRouter()

    def setup_routes(self):

        # Register User
        @self.router.post("/api/users/register-user")
        async def register_user_route(request: Request, response: Response):
            return await register_user_controller(request, response)

        # Get User
        @self.router.get("/api/users/get-user")
        async def get_user_route(request: Request, response: Response):
            return await get_user_controller(request, response)

        # Update User
        @self.router.put("/api/users/update-user")
        async def update_user_route(request: Request, response: Response):
            return await update_user_controller(request, response)

        # Delete User
        @self.router.delete("/api/users/delete-user")
        async def delete_user_route(request: Request, response: Response):
            return await delete_user_controller(request, response)

        return self.router     
