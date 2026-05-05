from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import EducationContent, UserEducationProgress
from app.schemas.schemas import EducationContentResponse, QuizSubmission, QuizResult

import uuid
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_education_content(
    language: str = None,
    db: Session = Depends(get_db),
):
    """Get all education content, optionally filtered by language."""
    query = db.query(EducationContent).filter(EducationContent.is_active == True)
    if language:
        query = query.filter(EducationContent.language == language)
    return query.all()


@router.get("/{content_id}", response_model=EducationContentResponse)
async def get_education_detail(content_id: str, db: Session = Depends(get_db)):
    """Get a single education content item."""
    content = db.query(EducationContent).filter(EducationContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.post("/quiz/submit", response_model=QuizResult)
async def submit_quiz(
    data: QuizSubmission,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit quiz answers and get score."""
    content = db.query(EducationContent).filter(EducationContent.id == data.content_id).first()
    if not content or content.content_type != "quiz":
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz_data = content.content
    correct = quiz_data.get("correct_answers", {})
    score = sum(1 for q, a in data.answers.items() if correct.get(q) == a)
    total = len(correct)

    # Save progress
    progress = UserEducationProgress(
        id=str(uuid.uuid4()),
        user_id=current_user["id"],
        content_id=data.content_id,
        completed=True,
        score=score,
        completed_at=datetime.utcnow(),
    )
    db.add(progress)
    db.commit()

    return QuizResult(score=score, total=total, correct_answers=correct)


@router.get("/progress")
async def get_progress(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's education progress."""
    progress = (
        db.query(UserEducationProgress)
        .filter(UserEducationProgress.user_id == current_user["id"])
        .all()
    )
    return {
        "completed": len([p for p in progress if p.completed]),
        "total": len(progress),
        "items": progress,
    }
