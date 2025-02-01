import json
from app.database.models import User
from fastapi import Request, Response, HTTPException, status

# register user controller
async def register_user_controller(request:Request, response:Response):
    request_body = await request.json()
    print(request_body['first_name'])
    return {"message": "User successefully registered!!!"}
