import json
from fastapi import Request, Response, HTTPException, status
from app.lib import AuthUtility
from app.database.models import User
from app.database import DB


# Update User
async def update_user_controller(request: Request, response:Response):
    
    # Retrieve decoded token from request body
    decoded_token = request.state.decoded_token        
    user_id = decoded_token['user_id'] 
    

    # Retrieving update data from request body
    request_body = await request.json()        
    first_name = request_body.get('first_name')
    last_name = request_body.get('last_name')
    email_address = request_body.get('email_address')
    user_name = request_body.get('user_name') 
    password = request_body.get('password')
    new_password = request_body.get('new_password')
    

    # Initialize the database connection
    db = DB()
    db.initialize()
    
    # Query the database and find the user to update
    user_to_update = db.session.query(User).filter(User.user_id == user_id).first()    
    
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    
    return "user updated"








