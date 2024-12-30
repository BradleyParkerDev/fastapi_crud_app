import json
from fastapi import Request, Response, HTTPException, status

# get user controller
async def get_user_controller(request:Request, response:Response):
    return {"message": "User data successefully retrieved!!!"}
