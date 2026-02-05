# src/api/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
   
Base = declarative_base()
   
class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       email = Column(String, unique=True)
       hashed_password = Column(String)
       is_active = Column(Boolean, default=True)
       created_at = Column(DateTime, default=datetime.utcnow)
   
class Query(Base):
       __tablename__ = "queries"
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       question = Column(String)
       answer = Column(String)
       cluster = Column(Integer, nullable=True)
       latency_ms = Column(Float)
       created_at = Column(DateTime, default=datetime.utcnow)