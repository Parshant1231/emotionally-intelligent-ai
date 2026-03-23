# backend/app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Stores user characteristics — feeds OBJ 2 analysis.
    (Which user traits affect engagement?)
    """
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True)
    session_id   = Column(String(100), unique=True, index=True)
    age_group    = Column(String(20))   # "18-24", "25-34", etc.
    gender       = Column(String(20))
    tech_comfort = Column(String(20))   # "low", "medium", "high"
    created_at   = Column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    """
    One row per conversation session.
    Tracks which bot was used and final satisfaction score.
    """
    __tablename__ = "chat_sessions"

    id              = Column(Integer, primary_key=True, index=True)
    session_id      = Column(String(100), index=True)
    user_session_id = Column(String(100))   # links to User
    bot_type        = Column(String(20))    # "ei" or "traditional"
    started_at      = Column(DateTime, default=datetime.utcnow)
    ended_at        = Column(DateTime, nullable=True)
    turn_count      = Column(Integer, default=0)
    satisfaction    = Column(Float, nullable=True)   # 1-5 rating
    sentiment_shift = Column(String(20), nullable=True)  # improved/stable/worsened


class ChatMessage(Base):
    """
    One row per message turn.
    Stores emotion data for every user message — feeds OBJ 3.
    """
    __tablename__ = "chat_messages"

    id                  = Column(Integer, primary_key=True, index=True)
    session_id          = Column(String(100), index=True)
    turn_number         = Column(Integer)
    role                = Column(String(10))   # "user" or "bot"
    content             = Column(Text)
    detected_emotion    = Column(String(20), nullable=True)
    emotion_confidence  = Column(Float, nullable=True)
    emotion_scores      = Column(JSON, nullable=True)
    style_applied       = Column(String(50), nullable=True)
    bot_type            = Column(String(20))
    timestamp           = Column(DateTime, default=datetime.utcnow)