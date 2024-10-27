import json
from fastapi import Request, Response, HTTPException, status
from app.lib import AuthUtility
from app.database.models import User
from app.database import DB

# Get User
async def get_user_controller(request: Request, response:Response):
    
    # Retrieve decoded token from request body
    decoded_token = request.state.decoded_token        
    user_id = decoded_token['user_id'] 
    
    # Initialize the database connection
    db = DB()
    db.initialize()
    
    # Query the database to find the user
    found_user = db.session.query(User).filter(User.user_id == user_id).first()
    
    print(f"found_user.first_name:{found_user.first_name}")
    
    # Close database connection
    db.close()
    
    # Create a dictionary (JSON object)
    user_data = {
        "user_id": found_user.user_id,
        "first_name": found_user.first_name,
        "last_name": found_user.last_name,
        "email_address": found_user.email_address,
        "user_name": found_user.user_name
    }
    
    return {"message":"user data retrieved", "user_data": user_data}
