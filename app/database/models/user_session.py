from sqlalchemy import Column, String, DateTime, ForeignKey  
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from .model_base_class import Base
from datetime import datetime, timedelta
import uuid

# Define the UserSession model
class UserSession(Base):
    __tablename__ = 'user_sessions'

    session_id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(pgUUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)  # Nullable for guests
    start_time = Column(DateTime, default=datetime.utcnow)  # Defaults to current time
    expiration_time = Column(DateTime, default=datetime.utcnow() + timedelta(days=7))  # Set to expire in 7 days

    @staticmethod
    def get_expiration_time():
        return datetime.utcnow() + timedelta(days=7)
