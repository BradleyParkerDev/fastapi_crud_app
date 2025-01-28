import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment varibles 
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class AuthTokenHelper:
    def __init__(self):
        self.jwt_secret_key = JWT_SECRET_KEY
        if not self.jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY environment variable not set!!!")
        
    def generate_session_token(self, session_payload):
        session_token = jwt.encode(session_payload, self.jwt_secret_key, algorithm="HS256")
        user_id = session_payload.get('user_id')
        if user_id:
            print(f"authenticated_session_token:\n{session_token}")
        else:
            print(f"guest_session_token:\n{session_token}")
        return session_token
    
    def verify_session_token(self, session_token):
        try:
            decoded_token = jwt.decode(session_token, self.jwt_secret_key, algorithms="HS256")
            return decoded_token
        except ExpiredSignatureError:
            print("Token has expired!!!")
            return None
        except InvalidTokenError:
            print("Invalid token!!!")
            return None