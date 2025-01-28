from app.database.models import UserSession
from app.database.db import DB
from sqlalchemy.exc import NoResultFound

class AuthSessionHelper:
    
    # Create session
    def create_user_session(self, user_id=None):
        db = DB()
        db.initialize()
        try:
            # Create a new user_session
            user_session = UserSession(user_id=user_id)

            # Add and commit the new session to the database
            db.session.add(user_session)
            db.session.commit()

            # Extract the data from the committed user_session
            session_data = {
                "user_id": str(user_session.user_id) if user_session.user_id else "", # Blank if guest_session
                "session_id": str(user_session.session_id),
                "start_time": user_session.start_time.isoformat(),
                "expiration_time": user_session.expiration_time.isoformat()
            }

            if user_id:
                print("\nAuthenticated user session created!!!\n")
            else:
                print("\nGuest user session created!!!\n")

        finally:
            db.close()


    # Delete session
    def delete_user_session(self, session_id):
        db = DB()
        db.initialize()

        try:
            # Query the session and delete it
            session_to_delete = db.session.query(UserSession).filter_by(session_id=session_id).one()
            db.session.delete(session_to_delete)
            db.session.commit()
            db.close()
            return True
        except NoResultFound:
            return False

    # Cron job - delete expired sessions
    def handle_expired_user_sessions_cron_job():
        return 