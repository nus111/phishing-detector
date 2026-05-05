import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, ForeignKey,
    JSON, Boolean, Text
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    preferred_language = Column(String, default="en")
    role = Column(String, default="user")  # "user" or "admin"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    analyses = relationship("AnalysisLog", back_populates="user", lazy="dynamic")
    education_progress = relationship("UserEducationProgress", back_populates="user", lazy="dynamic")
    feedback = relationship("Feedback", back_populates="user", lazy="dynamic")


class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    input_language = Column(String, default="en")
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # "low", "medium", "high"
    detected_patterns = Column(JSON, default=list)
    recommendation = Column(Text)
    model_version = Column(String, default="v1.0")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="analyses")


class EducationContent(Base):
    __tablename__ = "education_content"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # "tip", "quiz", "article"
    language = Column(String, nullable=False, index=True)
    difficulty_level = Column(String, default="beginner")
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress = relationship("UserEducationProgress", back_populates="content", lazy="dynamic")


class UserEducationProgress(Base):
    __tablename__ = "user_education_progress"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(String, ForeignKey("education_content.id"), nullable=False)
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="education_progress")
    content = relationship("EducationContent", back_populates="progress")


class ThreatReport(Base):
    __tablename__ = "threat_reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    region = Column(String)
    language = Column(String, index=True)
    threat_type = Column(String)
    count = Column(Integer, default=0)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    details = Column(JSON, default=dict)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    analysis_log_id = Column(String, ForeignKey("analysis_logs.id"))
    feedback_type = Column(String, nullable=False)  # "false_positive" or "false_negative"
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedback")
