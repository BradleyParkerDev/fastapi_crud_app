import os;
from app.database.models import SessionCronJob, UserSession 
from app.database.db import DB
from app.lib.logger import get_logger
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


class CronSessionHelper:
    def __init__(self):
        self.cron_logger = get_logger("cron")
        self.scheduler = BackgroundScheduler()
        self.job = None  # Keep a reference to the job

    def start_cron(self):
        if not self.scheduler.running:
            self.scheduler.start()
            self.cron_logger.info("Scheduler started.")
        
        # Avoid duplicating jobs
        if self.job is None:
            self.job = self.scheduler.add_job(
                self.handle_expired_user_sessions,
                'cron',
                minute='10,20,30,40,50,0',
                id='session-cleanup-job',
                replace_existing=True
            )
            self.cron_logger.info("Session cleanup job scheduled.")
        else:
            self.cron_logger.info("Session cleanup job already running.")

    def stop_cron(self):
        if self.scheduler.running:
            self.scheduler.remove_job('session-cleanup-job')
            self.job = None
            self.cron_logger.info("Session cleanup job stopped.")
            self.scheduler.shutdown()
            self.cron_logger.info("Scheduler shutdown.")

    def restart_cron(self):
        self.stop_cron()
        self.start_cron()

    def handle_expired_user_sessions(self):
        self.cron_logger.info(f"Running session cleanup at {datetime.now(timezone.utc)}...")

        db = DB()
        db.initialize()
        try:
            now = datetime.now(timezone.utc)
            expired_sessions = db.session.query(UserSession).filter(UserSession.expiration_time < now).all()
            num_deleted = len(expired_sessions)

            if num_deleted > 0:
                for session in expired_sessions:
                    db.session.delete(session)
                db.session.commit()

            self.cron_logger.info(f"{num_deleted} sessions deleted.")
            db.session.add(SessionCronJob(sessions_deleted=num_deleted))
            db.session.commit()
        except Exception as e:
            self.cron_logger.error(f"Error running cron job: {e}")
        finally:
            db.close()




# class CronSessionHelper():
#     def __init__(self):
#         self.cron_logger = get_logger("cron")
#         self.scheduler = BackgroundScheduler()
#         self.scheduler.add_job(self.handle_expired_user_sessions, 'cron', minute='10,20,30,40,50,0')

#         # Only start the scheduler if the RUN_SCHEDULER environment variable is "true"
#         if os.getenv("RUN_SCHEDULER", "false").lower() == "true":
#             self.start_session_cron_job()
#             # Ensure scheduler stops when the app shuts down
#             atexit.register(self.shutdown_scheduler)

#     # Ensure the scheduler runs only once
#     def start_session_cron_job(self):
#         if not self.scheduler.running:
#             self.scheduler.start()
#             self.cron_logger.info("Session cleanup cron job started.")

#     # Shutdown the scheduler when app stops
#     def shutdown_scheduler(self):
#         if self.scheduler.running:
#             self.scheduler.shutdown()
#             self.cron_logger.info("Session cleanup cron job stopped.")
    
#     # Deletes expired sessions
#     def handle_expired_user_sessions(self):

#         self.cron_logger.info(f"Running session cleanup at {datetime.now(timezone.utc)}...")

#         db = DB()
#         db.initialize()
#         try:
#             now = datetime.now(timezone.utc)

#             # Find expired sessions
#             expired_sessions = db.session.query(UserSession).filter(UserSession.expiration_time < now).all()
#             num_deleted = len(expired_sessions)

#             if num_deleted > 0:
#                 for session in expired_sessions:
#                     db.session.delete(session)
#                 db.session.commit()

#             # Log the cron job execution
#             self.cron_logger.info(f"{num_deleted} sessions deleted!!!")

#             # Store in the database
#             cron_job = SessionCronJob(sessions_deleted=num_deleted)
#             db.session.add(cron_job)
#             db.session.commit()

#         except Exception as e:
#             self.cron_logger.error(f"Error running cron job: {e}")
#         finally:
#             db.close()