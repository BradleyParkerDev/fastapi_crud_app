import json
from fastapi import Request, Response, HTTPException, status
from app.lib import AuthUtility
from app.database.models import User
from app.database import DB



# Delete User

async def delete_user_controller(request: Request, response:Response):
    
    # Retrieve decoded token from request body
    decoded_token = request.state.decoded_token
    user_id = decoded_token.get("user_id")

    # Initialize the database connection
    db = DB()
    db.initialize()
    
    # Query the database and find the user to delete
    user_to_delete = db.session.query(User).filter(User.user_id == user_id).first()
            
    db.session.delete(user_to_delete)
    
    db.session.commit()
    
    db.close()
    return {"message":"User successfully deleted!", "deleted_user": user_to_delete}
        
