from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.models import AnalysisLog, Feedback
from app.schemas.schemas import (
    AnalysisRequest, AnalysisResponse, AnalysisHistoryItem,
    PaginatedResponse, FeedbackCreate,
)
from app.services.phishing_detector import detect_phishing

router = APIRouter()


@router.post("", response_model=AnalysisResponse)
async def analyze_message(
    data: AnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyze a message for phishing/fraud indicators."""
    result = await detect_phishing(data.text, data.language)

    log = AnalysisLog(
        user_id=current_user["id"],
        input_text=data.text,
        input_language=result["detected_language"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        detected_patterns=result["detected_patterns"],
        recommendation=result["recommendation"],
        model_version=result["model_version"],
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return AnalysisResponse(
        id=log.id,
        input_text=log.input_text,
        detected_language=log.input_language,
        risk_score=log.risk_score,
        risk_level=log.risk_level,
        detected_patterns=result["detected_patterns"],
        recommendation=log.recommendation,
        model_version=log.model_version,
        created_at=log.created_at,
    )


@router.get("/history", response_model=PaginatedResponse)
async def get_history(
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's analysis history with pagination."""
    offset = (page - 1) * limit
    query = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.user_id == current_user["id"])
    )
    total = query.count()
    items = (
        query.order_by(AnalysisLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return PaginatedResponse(items=items, total=total, page=page, limit=limit)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_detail(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get details of a specific analysis."""
    log = (
        db.query(AnalysisLog)
        .filter(
            AnalysisLog.id == analysis_id,
            AnalysisLog.user_id == current_user["id"],
        )
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return AnalysisResponse(
        id=log.id,
        input_text=log.input_text,
        detected_language=log.input_language,
        risk_score=log.risk_score,
        risk_level=log.risk_level,
        detected_patterns=log.detected_patterns or [],
        recommendation=log.recommendation,
        model_version=log.model_version,
        created_at=log.created_at,
    )


@router.post("/feedback", status_code=201)
async def submit_feedback(
    data: FeedbackCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit feedback on an analysis (false positive/negative)."""
    fb = Feedback(
        user_id=current_user["id"],
        analysis_log_id=data.analysis_log_id,
        feedback_type=data.feedback_type,
        description=data.description,
    )
    db.add(fb)
    db.commit()
    return {"message": "Feedback submitted", "id": fb.id}
