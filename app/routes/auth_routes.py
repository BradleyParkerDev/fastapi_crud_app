from fastapi import APIRouter, Request, Response
from app.controllers import login_user_controller, logout_user_controller

# Auth API
class AuthRoutes:
    def __init__(self):
        self.router = APIRouter()
            
    def setup_routes(self):
        
        # Login User
        @self.router.post("/api/auth/login-user")   
        async def login_user_route(request:Request, response:Response):
            return await login_user_controller(request,response)
    
        # Logout User
        @self.router.delete("/api/auth/logout-user")   
        async def logout_user_route(request:Request,response:Response):
            return await logout_user_controller(request,response)
         
        return self.router
    
    
