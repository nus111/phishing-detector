from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ── Auth ──
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    preferred_language: str = "en"


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    preferred_language: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Analysis ──
class AnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = None  # auto-detect if None


class DetectedPattern(BaseModel):
    type: str
    confidence: float
    evidence: str
    explanation: str


class AnalysisResponse(BaseModel):
    id: str
    input_text: str
    detected_language: str
    risk_score: float
    risk_level: str
    detected_patterns: List[DetectedPattern]
    recommendation: str
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisHistoryItem(BaseModel):
    id: str
    input_text: str
    detected_language: str
    risk_score: float
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int


# ── Education ──
class EducationContentResponse(BaseModel):
    id: str
    title: str
    content_type: str
    language: str
    difficulty_level: str
    content: Dict[str, Any]

    class Config:
        from_attributes = True


class QuizSubmission(BaseModel):
    content_id: str
    answers: Dict[str, str]


class QuizResult(BaseModel):
    score: int
    total: int
    correct_answers: Dict[str, str]


# ── Feedback ──
class FeedbackCreate(BaseModel):
    analysis_log_id: str
    feedback_type: str  # "false_positive" or "false_negative"
    description: Optional[str] = None


# ── Admin ──
class DashboardStats(BaseModel):
    total_analyses: int
    total_users: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    analyses_by_language: Dict[str, int]
    analyses_by_day: List[Dict[str, Any]]
    recent_threats: List[Dict[str, Any]]
