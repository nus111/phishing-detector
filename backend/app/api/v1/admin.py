from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

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

    # Risk level counts
    risk_counts = dict(
        db.query(AnalysisLog.risk_level, func.count(AnalysisLog.id))
        .group_by(AnalysisLog.risk_level)
        .all()
    )

    # Analyses by language
    lang_counts = dict(
        db.query(
            func.coalesce(AnalysisLog.input_language, "unknown"),
            func.count(AnalysisLog.id),
        )
        .group_by(AnalysisLog.input_language)
        .all()
    )

    # Analyses by day (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_raw = (
        db.query(
            func.date(AnalysisLog.created_at).label("day"),
            func.count(AnalysisLog.id),
        )
        .filter(AnalysisLog.created_at >= thirty_days_ago)
        .group_by(func.date(AnalysisLog.created_at))
        .order_by(func.date(AnalysisLog.created_at))
        .all()
    )
    analyses_by_day = [{"date": str(d), "count": c} for d, c in daily_raw]

    # Recent high-risk analyses
    recent_high = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.risk_level == "high")
        .order_by(AnalysisLog.created_at.desc())
        .limit(10)
        .all()
    )
    recent_threats = [
        {
            "id": r.id,
            "language": r.input_language,
            "risk_score": r.risk_score,
            "patterns": [p.get("type") for p in (r.detected_patterns or [])],
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in recent_high
    ]

    return DashboardStats(
        total_analyses=total_analyses,
        total_users=total_users,
        high_risk_count=risk_counts.get("high", 0),
        medium_risk_count=risk_counts.get("medium", 0),
        low_risk_count=risk_counts.get("low", 0),
        analyses_by_language=lang_counts,
        analyses_by_day=analyses_by_day,
        recent_threats=recent_threats,
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
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role,
            "preferred_language": u.preferred_language,
            "created_at": u.created_at,
            "analysis_count": u.analyses.count(),
        }
        for u in users
    ]


@router.post("/retrain")
async def trigger_retrain(
    admin_user: dict = Depends(require_admin),
):
    """Trigger model retraining (placeholder)."""
    # TODO: Send retrain request to ML service
    return {
        "status": "queued",
        "message": "Model retraining has been queued. This may take a while.",
    }


@router.get("/feedback")
async def get_feedback(
    admin_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all user feedback."""
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return [
        {
            "id": f.id,
            "user_id": f.user_id,
            "analysis_log_id": f.analysis_log_id,
            "feedback_type": f.feedback_type,
            "description": f.description,
            "created_at": f.created_at,
        }
        for f in feedbacks
    ]
