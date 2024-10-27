import json
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from app.lib import AuthUtility
from app.database.models import User, UserSession
from app.database import DB

async def logout_user_controller( request:Request, response:Response):
    # Access the decoded token from request.state
    decoded_token = request.state.decoded_token        
    session_id = decoded_token['session_id']
    print(f"session_id: {session_id}")
    auth_util = AuthUtility()
    auth_util.session.delete_user_session(session_id)
    
    response.delete_cookie('session_cookie')
    # redirect to index page
    
    
    return 'User successfully logged out!'