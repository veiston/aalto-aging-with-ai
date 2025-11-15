from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, delete

from ..database import get_session
from ..models import Survey, Question

router = APIRouter(
    prefix="/surveys",
    tags=["surveys"]
)

@router.post("/")
def create_survey(payload: dict, session: Session = Depends(get_session)):
    survey = Survey(
        title=payload["title"],
        description=payload["description"],
        user_id=payload.get("user_id")
    )
    session.add(survey)
    session.commit()
    session.refresh(survey)

    for q in payload.get("questions", []):
        question = Question(
            survey_id=survey.id,
            type=q["type"],
            text=q["text"],
            required=q.get("required", False),
            options=q.get("options")
        )
        session.add(question)

    session.commit()
    return survey


@router.get("/")
def list_surveys(session: Session = Depends(get_session)):
    surveys = session.exec(select(Survey)).all()
    return surveys


@router.get("/{survey_id}")
def get_survey(survey_id: int, session: Session = Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


@router.delete("/{survey_id}")
def delete_survey(survey_id: int, session: Session = Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    session.exec(delete(Question).where(Question.survey_id == survey_id))
    session.delete(survey)
    session.commit()

    return {"status": "deleted"}