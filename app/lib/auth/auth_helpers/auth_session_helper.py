from app.database.models import UserSession
from app.database import DB
from sqlalchemy.exc import NoResultFound

class AuthSessionHelper:

    # Create user_session
    def create_user_session(self, user_id=None):
        db = DB()
        db.initialize()
        
        try:
            user_session = UserSession()
            
            if user_id:
                user_session.user_id = user_id
            
            db.session.add(user_session)
            db.session.commit()
            
            # Extract needed data before closing the session
            session_data = {
                "session_id": str(user_session.session_id),
                "start_time": user_session.start_time.isoformat(),  # Convert to ISO string
                "exp": user_session.expiration_time.isoformat()  # Convert to ISO string
            }
            
            print(f"\nUser session created!\n")
            return session_data
        
        finally:
            db.close()

        
    # Delete user_session
    def delete_user_session(self,session_id):
        db = DB()
        db.initialize()
        
        try:
            # Query the session and delete it
            session_to_delete = db.session.query(UserSession).filter_by(session_id=session_id).one()
            db.session.delete(session_to_delete)
            db.session.commit()
            db.close()
            return 'User session deleted!'
        except NoResultFound:
            return 'Session not found!'
    
    # Delete expired user_sessions
    def delete_expired_sessions():
        return 'Expired sessions deleted!'