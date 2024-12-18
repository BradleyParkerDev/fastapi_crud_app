# import json
# from fastapi import Request, Response, HTTPException, status
# from fastapi.responses import RedirectResponse
# from app.lib import AuthUtility
# from app.database.models import User, UserSession
# from app.database import DB


# async def login_user_controller(request:Request, response:Response):
#     # Retrieve and parse the request body
#     request_body = await request.json()

#     # Extract email and password from the request
#     email_address = request_body.get('email_address')
#     password = request_body.get('password')

#     # Ensure both email and password are provided
#     if not email_address or not password:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing email or password")

#     auth = AuthUtility()
    
#     # Initialize the database after retrieving the request body
#     db = DB()
#     db.initialize()
    
#     # Find user in database
#     found_user = db.session.query(User).filter(User.email_address == email_address).first()
    
    
#     # find user
#     # validate password
#     passwords_match = auth.validate_password(password, found_user.password)
    
#     print(f"Passwords match: {passwords_match}")
    
#     if passwords_match: 
#         # create an authenticated user session
#         authenticated_session = auth.session.create_user_session(found_user.user_id)
        
#         # create dict with session information
#         authenticated_session_payload = {
#             "user_id": authenticated_session['user_id'],  # Make sure values are serializable
#             "session_id": authenticated_session['session_id'],
#             "start_time": authenticated_session['start_time'],  # Convert datetime to string
#             "exp": authenticated_session['expiration_time']  # Convert datetime to string
#         }
        
#         # store session information in JSON Web Token as its payload
#         authenticated_session_token = auth.token.generate_session_token(authenticated_session_payload)
    
#     # close database connection 
#     db.close()
    
    
#     # Set "session_cookie" in response, with "authenticated_session_token" as its value 
#     response.set_cookie(key="session_cookie", value = authenticated_session_token, httponly=True, expires=authenticated_session.expiration_time)  
    
         
#      # redirect to authenticated_user_page
     
     
     
                 
#     return "User successfully logged in!"




import json
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from app.lib import AuthUtility
from app.database.models import User, UserSession
from app.database import DB


async def login_user_controller(request: Request, response: Response):
    # Retrieve and parse the request body
    request_body = await request.json()

    # Extract email and password from the request
    email_address = request_body.get('email_address')
    password = request_body.get('password')

    print(email_address)
    print(password)
    # Ensure both email and password are provided
    if not email_address or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing email or password")

    auth = AuthUtility()
    
    # Initialize the database after retrieving the request body
    db = DB()
    db.initialize()
    
    # Find user in database
    found_user = db.session.query(User).filter(User.email_address == email_address).first()
    
    # Check if user exists
    if not found_user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Validate password
    passwords_match = auth.validate_password(password, found_user.password)
    print(f"Passwords match: {passwords_match}")
    
    if not passwords_match:
        db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    # Create an authenticated user session if the password is correct
    print(f"Found User ID: {found_user.user_id}")
    authenticated_session = auth.session.create_user_session(found_user.user_id)
    print(authenticated_session)    
    # Create dict with session information
    authenticated_session_payload = {
        "user_id": str(authenticated_session['user_id']),  # Ensure values are serializable
        "session_id": str(authenticated_session['session_id']),
        "start_time": authenticated_session['start_time'],  
        "exp": authenticated_session['expiration_time']  
    }
    
    # Store session information in JSON Web Token as its payload
    authenticated_session_token = auth.token.generate_session_token(authenticated_session_payload)
    
    print(authenticated_session_token)
    # Close database connection 
    db.close()
    
    # Set "session_cookie" in response, with "authenticated_session_token" as its value
    response.set_cookie(
        key="session_cookie", 
        value=authenticated_session_token, 
        httponly=True, 
        expires=authenticated_session['expiration_time']
    )
    
    # Redirect to the authenticated user page
    return {"success":"true", "message": "User registered successfully"}
