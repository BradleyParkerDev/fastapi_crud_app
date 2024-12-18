import bcrypt
from fastapi import Request, Response
from app.lib import AuthSessionHelper, AuthTokenHelper

# Auth Util
class AuthUtility:
    
    def __init__(self):
        self.session = AuthSessionHelper()   
        self.token = AuthTokenHelper()     


    # Hash Password
    def generate_hash_password(self, new_password, salt_rounds):
        # The password should be used directly without hardcoding
        # Ensure that the password is in bytes
        new_password = new_password.encode('utf-8')
        
        # Custom number of salt rounds (e.g., 5 rounds)
        salt = bcrypt.gensalt(rounds=salt_rounds)

        # Hash the password with the custom salt rounds
        hashed_password = bcrypt.hashpw(new_password, salt)

        print(f"hashed_password: {hashed_password}")

        # Decode hashed_password if necessary (assuming database expects a string)
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode('utf-8')               
        return hashed_password



    # Validate Password
    def validate_password(self, password, hashed_password):
        # hashed_password should already be in bytes, so don't encode it again
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        
        print(f"hashed_password: {hashed_password}")
        
        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
        else:
            return False
        
    
    
    async def authorize_user(self, request: Request, call_next):
        print("\nAuthorization Middleware!!!\n")
        
        # Get the session token from cookies
        session_token = request.cookies.get('session_cookie')
        
        # If there is a session, decode its token
        if session_token:
            print(f"session_token:\n{session_token}\n")
            
            # Decode the token (assuming token verification method is async)
            decoded_token = self.token.verify_session_token(session_token)
            
            if decoded_token:
                # Proceed with authenticated user
                if "user_id" in decoded_token:
                    print("Authenticated User:")
                    print(f"user_id: {decoded_token['user_id']}")
                    print(f"session_id: {decoded_token['session_id']}")
                    print(f"start_time: {decoded_token['start_time']}")
                    print(f"exp: {decoded_token['exp']}\n")
                else:
                    print("Guest User:")
                    print(f"session_id: {decoded_token['session_id']}")
                    print(f"start_time: {decoded_token['start_time']}")
                    print(f"exp: {decoded_token['exp']}\n")
                request.state.decoded_token = decoded_token
            else:
                print("Invalid or expired token")
                            
            # Store the decoded token in request.state for later use in the request lifecycle
            request.state.decoded_token = decoded_token
            
            # Proceed to the next middleware or endpoint
            response = await call_next(request)
        
        # If there is no session token, create a guest session
        else:
            guest_session = self.session.create_user_session()
            
            # Create dictionary with session information, ensuring primitive types
            guest_session_payload = {
                "session_id": guest_session['session_id'],
                "start_time": guest_session['start_time'],
                "exp": guest_session['exp']
            }            
            
            # Generate a guest session token
            guest_session_token = self.token.generate_session_token(guest_session_payload)
            
            # Process request and set the guest session cookie
            response = await call_next(request)
            response.set_cookie(key="session_cookie", value=guest_session_token, httponly=True)
        
        return response