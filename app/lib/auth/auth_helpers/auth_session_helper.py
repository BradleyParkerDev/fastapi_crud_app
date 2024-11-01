from app.database.models import UserSession
from app.database import DB
from sqlalchemy.exc import NoResultFound

class AuthSessionHelper:

    # Session Methods
    # Create user_session
    def create_user_session(self, user_id=None):
        db = DB()
        db.initialize()
        
        user_session = UserSession()
        
        # If user is logging in add their user_id to the session
        if user_id:
            user_session.user_id = user_id
            
        db.session.add(user_session)
        
        db.session.commit()
        
        # db.session.close()
        print(f"\nUser session created!!!\n")
        
        return user_session
        
        # return 'User session created!'
        
    # Delete user_session
    def delete_user_session(self,session_id):
        db = DB()
        db.initialize()
        
        try:
            # Query the session and delete it
            session_to_delete = db.session.query(UserSession).filter_by(session_id=session_id).one()
            db.session.delete(session_to_delete)
            db.session.commit()
            return 'User session deleted!'
        except NoResultFound:
            return 'Session not found!'
    
    # Delete expired user_sessions
    def delete_expired_sessions():
        return 'Expired sessions deleted!'