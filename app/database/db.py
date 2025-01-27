import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, UserSession, User

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# For CRUD operations
class DB:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.session_local = None
        self.session = None

    def initialize(self):
        self.engine = create_engine(self.database_url,echo=True)
        self.session_local = sessionmaker(bind=self.engine)
        self.session = self.session_local()

    def close(self):
        if self.session:
            self.session.close

# For db creation without alembic
engine = create_engine(DATABASE_URL, echo=True)
def init_db():
    print("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    print("App successfully connected to database!!!")