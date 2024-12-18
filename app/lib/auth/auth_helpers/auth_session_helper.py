from app.database.models import UserSession
from app.database import DB
from sqlalchemy.exc import NoResultFound

class AuthSessionHelper:

    # Create user_session
    def create_user_session(self, user_id=None):
        db = DB()
        db.initialize()

        try:
            # Create a new UserSession with the provided user_id (or None for guest session)
            user_session = UserSession(user_id=user_id)

            # Add and commit the new session to the database
            db.session.add(user_session)
            db.session.commit()

            # Extract session data after committing to ensure values are set
            session_data = {
                "user_id": str(user_session.user_id) if user_session.user_id else "",  # Blank if guest session
                "session_id": str(user_session.session_id),
                "start_time": user_session.start_time.isoformat(),
                "expiration_time": user_session.expiration_time.isoformat()
            }

            # Print message based on session type
            if user_id:
                print("\nUser session created!\n")
            else:
                print("\nGuest session created!\n")

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