from app.database.models import SessionCronJob, UserSession 
from app.database.db import DB
from app.lib.exc import UserSessionExpired
from app.lib.logger import get_logger
from sqlalchemy.exc import NoResultFound
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
import atexit

class AuthSessionHelper:
    def __init__(self):
        self.user_logger = get_logger("user")
        self.cron_logger = get_logger("cron")
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handle_expired_user_sessions, 'cron', minute='10,20,30,40,50,0')

        # Start scheduler immediately
        self.start_session_cron_job()

        # Ensure scheduler stops when the app shuts down
        atexit.register(self.shutdown_scheduler)

    # Ensure the scheduler runs only once
    def start_session_cron_job(self):
        if not self.scheduler.running:
            self.scheduler.start()
            self.cron_logger.info("Session cleanup cron job started.")

    # Shutdown the scheduler when app stops
    def shutdown_scheduler(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.cron_logger.info("Session cleanup cron job stopped.")

    # Create Session
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
        
        return session_data
    
    # Get Session
    def get_user_session(self,session_id):
        db = DB()
        db.initialize()
        try:
            found_session = db.session.query(UserSession).filter_by(session_id=session_id).one()
            expiration_time = found_session.expiration_time
      
            # Ensure expiration_time is timezone-aware
            if expiration_time.tzinfo is None:
                expiration_time = expiration_time.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)  # Always use timezone-aware datetime
            is_expired = expiration_time < now
            
            print(f"Current Time: {now}, Expiration Time: {expiration_time}, is_expired: {is_expired}")
            if is_expired:
                db.session.delete(found_session)
                db.session.commit()
                db.close()
                raise UserSessionExpired
            return found_session
        except NoResultFound as e:
            raise ValueError(e)
        finally:
            db.close()

    # Delete Session
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

    # Session Cron Job - handles expired sessions on a schedule
    def start_session_cron_job(self):
        return self.scheduler.start()

    # Deletes expired sessions
    def handle_expired_user_sessions(self):

        self.cron_logger.info(f"Running session cleanup at {datetime.now(timezone.utc)}...")
        
        db = DB()
        db.initialize()
        try:
            now = datetime.now(timezone.utc)

            # Find expired sessions
            expired_sessions = db.session.query(UserSession).filter(UserSession.expiration_time < now).all()
            num_deleted = len(expired_sessions)

            if num_deleted > 0:
                for session in expired_sessions:
                    db.session.delete(session)
                db.session.commit()

            # Log the cron job execution
            self.cron_logger.info(f"{num_deleted} sessions deleted!!!")

            # Store in the database
            cron_job = SessionCronJob(sessions_deleted=num_deleted)
            db.session.add(cron_job)
            db.session.commit()

        except Exception as e:
            self.cron_logger.error(f"Error running cron job: {e}")
        finally:
            db.close()