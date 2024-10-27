import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

class AuthTokenHelper:
    # Access an environment variable for the secret key
    def __init__(self):
        self.jwt_secret_key = os.getenv('SECRET_KEY')
    
    # Generate a session token
    def generate_session_token(self, session_payload):
        # Create the token using HS256 algorithm
        session_token = jwt.encode(session_payload, self.jwt_secret_key, algorithm="HS256")
        
        user_id = session_payload.get('user_id')
        if user_id:  
            print(f"authenticated_session_token: {session_token}")
        else:
            print(f"guest_session_token: {session_token}")
        return session_token
    
    # Verify and decode the session token
    def verify_session_token(self, session_token):
        try:
            # Decode the token (convert to bytes if it's a string)
            decoded_token = jwt.decode(session_token, self.jwt_secret_key, algorithms=["HS256"])
            return decoded_token  # Return the decoded payload
        except ExpiredSignatureError:
            print("Token has expired")
            return None
        except InvalidTokenError:
            print("Invalid token")
            return None

    