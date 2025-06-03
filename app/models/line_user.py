from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.models.base import Base

class LineUser(Base):
    __tablename__ = "line_users"

    id = Column(Integer, primary_key=True, index=True)
    line_uid = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)