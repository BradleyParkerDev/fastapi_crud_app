import json
from fastapi import Request, Response, HTTPException, status
from app.lib import AuthUtility
from app.database.models import User
from app.database import DB




# Register User
async def register_user_controller(request: Request, response:Response):
    request_body = await request.json()
    print(f"first name: {request_body['first_name']}")
    first_name = request_body.get('first_name')
    print(first_name)
    

    first_name = request_body.get('first_name')
    last_name = request_body.get('last_name')
    email_address = request_body.get('email_address')
    user_name = request_body.get('user_name')
    password = request_body.get('password')
    
    
    db = DB()
    db.initialize()
    
    auth_util = AuthUtility()
    
    hashed_password = auth_util.generate_hash_password(password, 5)
    # new_user = User(body['email_address'], hashed_password)
            

    try:
        # Create a new User instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            user_name=user_name,
            password=hashed_password
        )

        # Add the new user to the session
        db.session.add(new_user)

        # Commit the transaction to save the user to the database
        db.session.commit()

        return {"message": "User registered successfully"}

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    finally:
        db.close()  # Ensure the session is closed