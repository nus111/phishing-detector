from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, AnalysisLog, Feedback, ThreatReport
from app.schemas.schemas import DashboardStats

router = APIRouter()


def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency: require admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    admin_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get admin dashboard statistics."""
    total_analyses = db.query(AnalysisLog).count()
    total_users = db.query(User).count()
    high_risk = db.query(AnalysisLog).filter(AnalysisLog.risk_level == "high").count()
    medium_risk = db.query(AnalysisLog).filter(AnalysisLog.risk_level == "medium").count()
    low_risk = db.query(AnalysisLog).filter(AnalysisLog.risk_level == "low").count()

    # Analyses by language
    lang_counts = (
        db.query(AnalysisLog.input_language, func.count(AnalysisLog.id))
        .group_by(AnalysisLog.input_language)
        .all()
    )
    analyses_by_language = {lang or "unknown": count for lang, count in lang_counts}

    return DashboardStats(
        total_analyses=total_analyses,
        total_users=total_users,
        high_risk_count=high_risk,
        medium_risk_count=medium_risk,
        low_risk_count=low_risk,
        analyses_by_language=analyses_by_language,
        recent_threats=[],
    )


@router.get("/threats")
async def get_threats(
    language: str = None,
    admin_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get threat trend data."""
    query = db.query(ThreatReport)
    if language:
        query = query.filter(ThreatReport.language == language)
    return query.order_by(ThreatReport.period_start.desc()).limit(50).all()


@router.get("/users")
async def get_users(
    admin_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all users."""
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/retrain")
async def trigger_retrain(
    admin_user: dict = Depends(require_admin),
):
    """Trigger model retraining (placeholder)."""
    # TODO: Send retrain request to ML service
    return {"status": "retrain_queued", "message": "Model retraining has been queued."}


@router.get("/feedback")
async def get_feedback(
    admin_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all user feedback."""
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
