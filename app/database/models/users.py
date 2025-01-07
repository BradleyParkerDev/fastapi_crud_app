import uuid
from .model_base_class import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_image = Column(String, nullable=True)  # Optional field for user image
    first_name = Column(String, nullable=False)  # Not nullable text field
    last_name = Column(String, nullable=False)  # Not nullable text field
    email_address = Column(String, unique=True, nullable=False)  # Unique and not nullable
    user_name = Column(String, unique=True, nullable=False)  # Unique and not nullable
    password = Column(String, nullable=False)  # Not nullable password field
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)  # Automatically sets current timestamp


