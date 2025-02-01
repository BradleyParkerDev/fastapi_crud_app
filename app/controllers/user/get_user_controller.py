import json
from fastapi import Request, Response, HTTPException, status

# get user controller
async def get_user_controller(request:Request, response:Response):
    print(f"session_id: {request.state.session_data['session_id']}")
    return {"message": "User data successefully retrieved!!!"}
