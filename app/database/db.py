import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .models import User, UserSession, Base  # Import Base along with your model

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class DB:
    def __init__(self):
        # Fetch the database URL from environment variables
        # self.model_base_class = declarative_base()
        self.database_url = DATABASE_URL
        self.engine = None
        self.Session = None
        self.session = None

    def initialize(self):
        # Use the correct instance variable for the database URL
        self.engine = create_engine(self.database_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def close(self):
        # Ensure the session is closed properly
        if self.session:
            self.session.close()






# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
# engine = create_engine(TEST_DATABASE_URL, echo=True)

def init_db():
  
    """Initialize the database and create tables."""
    print(f"Connecting to database at {DATABASE_URL}")
    
    # Create tables based on the Base metadata
    Base.metadata.create_all(bind=engine)
    
    print("Tables created successfully!")



