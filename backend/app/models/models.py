from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    preferred_language = Column(String, default="en")
    role = Column(String, default="user")  # "user" or "admin"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    analyses = relationship("AnalysisLog", back_populates="user")
    education_progress = relationship("UserEducationProgress", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")


class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    input_text = Column(Text, nullable=False)
    input_language = Column(String)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # "low", "medium", "high"
    detected_patterns = Column(JSON)
    recommendation = Column(Text)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")


class EducationContent(Base):
    __tablename__ = "education_content"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # "tip", "quiz", "article"
    language = Column(String, nullable=False)
    difficulty_level = Column(String, default="beginner")
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress = relationship("UserEducationProgress", back_populates="content")


class UserEducationProgress(Base):
    __tablename__ = "user_education_progress"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content_id = Column(String, ForeignKey("education_content.id"), nullable=False)
    completed = Column(Boolean, default=False)
    score = Column(Integer)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="education_progress")
    content = relationship("EducationContent", back_populates="progress")


class ThreatReport(Base):
    __tablename__ = "threat_reports"

    id = Column(String, primary_key=True)
    region = Column(String)
    language = Column(String)
    threat_type = Column(String)
    count = Column(Integer, default=0)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    details = Column(JSON)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    analysis_log_id = Column(String, ForeignKey("analysis_logs.id"))
    feedback_type = Column(String, nullable=False)  # "false_positive", "false_negative"
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedback")
