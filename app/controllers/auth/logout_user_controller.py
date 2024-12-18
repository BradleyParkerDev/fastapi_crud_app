import json
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from app.lib import AuthUtility
from app.database.models import User, UserSession
from app.database import DB

async def logout_user_controller( request:Request, response:Response):
    # Access the decoded token from request.state
    decoded_token = request.state.decoded_token        
    session_id = decoded_token['session_id']


    auth = AuthUtility()
    auth.session.delete_user_session(session_id)
    
    response.delete_cookie('session_cookie')
    # redirect to index page
    
    print(f"\nUser successfully logged out!\n")
    
    # Return a JSON response or redirect, as desired
    return JSONResponse(content={"success": "true", "message": "User successfully logged out!"})