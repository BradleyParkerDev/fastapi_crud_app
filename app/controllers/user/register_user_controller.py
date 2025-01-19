import json
from fastapi import Request, Response, HTTPException, status

# register user controller
async def register_user_controller(request:Request, response:Response):
    return {"message": "User successefully registered!!!"}
