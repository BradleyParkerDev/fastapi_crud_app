from sqlalchemy import Column, String, DateTime, ForeignKey  
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from .model_base_class import Base
from datetime import datetime, timedelta, timezone
import uuid

# Define the UserSession model
class UserSession(Base):
    __tablename__ = 'user_sessions'

    session_id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(pgUUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)  # Nullable for guests
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Defaults to current UTC time
    expiration_time = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=7))  # Expires in 7 days

    @staticmethod
    def get_expiration_time():
        return datetime.now(timezone.utc) + timedelta(days=7)
