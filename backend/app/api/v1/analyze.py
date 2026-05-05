from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.models import AnalysisLog
from app.schemas.schemas import AnalysisRequest, AnalysisResponse

router = APIRouter()


@router.post("", response_model=AnalysisResponse)
async def analyze_message(
    data: AnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Analyze a message for phishing/fraud indicators.
    Sends text to ML service for classification.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/predict",
                json={"text": data.text, "language": data.language},
            )
            response.raise_for_status()
            result = response.json()
    except httpx.RequestError:
        # Fallback: return mock result if ML service is down
        result = {
            "risk_score": 50.0,
            "risk_level": "medium",
            "detected_language": data.language or "unknown",
            "detected_patterns": [],
            "recommendation": "ML service unavailable. Please try again later.",
            "model_version": "offline",
        }

    # Save to database
    log = AnalysisLog(
        id=str(uuid.uuid4()),
        user_id=current_user["id"],
        input_text=data.text,
        input_language=result.get("detected_language"),
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        detected_patterns=result.get("detected_patterns"),
        recommendation=result.get("recommendation"),
        model_version=result.get("model_version"),
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
        detected_patterns=result.get("detected_patterns", []),
        recommendation=log.recommendation,
        model_version=log.model_version,
        created_at=log.created_at,
    )


@router.get("/history")
async def get_history(
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's analysis history with pagination."""
    offset = (page - 1) * limit
    logs = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.user_id == current_user["id"])
        .order_by(AnalysisLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.user_id == current_user["id"])
        .count()
    )
    return {
        "items": logs,
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_detail(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get details of a specific analysis."""
    log = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.id == analysis_id, AnalysisLog.user_id == current_user["id"])
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return log
