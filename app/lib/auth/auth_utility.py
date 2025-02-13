import bcrypt
from fastapi import Request, Response
from .auth_helpers import AuthSessionHelper, AuthTokenHelper
from app.lib.exc import UserSessionExpired

class AuthUtility():
    def __init__(self):
        self.session = AuthSessionHelper()
        self.token = AuthTokenHelper()

    # Hash Password
    def generate_password_hash(self, new_password, salt_rounds):
        try:
            # Encode the password to bytes
            new_password = new_password.encode('utf-8')

            # Generate salt with the specified number of rounds
            salt = bcrypt.gensalt(rounds=salt_rounds)

            # Hash the password with the generated salt
            hashed_password = bcrypt.hashpw(new_password, salt)

            # Decode the hashed password to a string and return
            return hashed_password.decode('utf-8')
        except Exception as e:
            print(f"Error generating password hash: {e}")
            return None

    # Validate Password
    def validate_password(self, password, hashed_password):
        try:
            # Convert the hashed password to bytes
            hashed_password = hashed_password.encode('utf-8')

            # Check if the password matches the hash
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except Exception as e:
            print(f"Error validating password: {e}")
            return False
        
    # Create Guest Session
    def create_guest_session_and_token(self):
        guest_session = self.session.create_user_session()
        token_payload = {
            "session_type": "guest",
            "session_id": guest_session['session_id'],
            "start_time": guest_session['start_time'],
            "exp": guest_session['expiration_time']            
        }
        guest_session_token = self.token.generate_session_token(token_payload)
        return {"token": guest_session_token, "payload": token_payload}

    # Middleware 
    async def authorize_user(self, request: Request, call_next):

        print("\nAuthorization Middleware!!!")

        # Retrieve session token from the request
        session_token = request.cookies.get("session_cookie")
        guest_session_data = None  # Ensure it's always defined

        # If a session token is present, attempt to decode it
        if session_token:
            print(f"\nsession_token:\n{session_token}\n")
            try:
                decoded_token = self.token.verify_session_token(session_token)
                if decoded_token:
                    try:
                        # Check if session exists in the database
                        found_session = self.session.get_user_session(decoded_token['session_id'])
                        print(f"session_type: {decoded_token['session_type']}")
                        print(f"user_id: {decoded_token.get(' user_id') or 'N/A'}")
                        print(f"session_id: {decoded_token['session_id']}")
                        print(f"start_time: {decoded_token['start_time']}")
                        print(f"exp: {decoded_token['exp']}\n")
                        request.state.session_data = decoded_token                              
                    except UserSessionExpired as e:
                        print(f"Session Expired: {e}\n")
                        print("Deleting user session and token...")
                        self.session.delete_user_session(decoded_token['session_id'])
                        session_token = None

            except (ValueError, Exception) as e:
                print(f"Error: {e}\n")
                session_token = None

        # If there's no valid session token
        if not session_token:
            print("session_token not found or invalid...")
            guest_session_data = self.create_guest_session_and_token()
            session_token = guest_session_data['token']
            request.state.session_data = guest_session_data['payload']

        response = await call_next(request) 

        # Only set a session cookie if a new session was created
        if guest_session_data:
            response.set_cookie(key="session_cookie", value=session_token, httponly=True)

        return response
 