from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/surveys")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.SurveyOut)
def create_survey(data: schemas.SurveyCreate, db: Session = Depends(get_db)):
    survey = models.Survey(
        title=data.title,
        payload={"questions": [q.dict() for q in data.questions]},
        status="draft",
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey


@router.get("")
def list_surveys(db: Session = Depends(get_db)):
    surveys = db.query(models.Survey).all()
    output = []
    for s in surveys:
        output.append({
            "id": s.id,
            "title": s.title,
            "status": s.status,
            "responses": len(s.responses)
        })
    return output


@router.get("/{survey_id}")
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    responses = db.query(models.Response).filter(models.Response.survey_id == survey_id).all()

    return {
        "survey": {
            "id": survey.id,
            "title": survey.title,
            "status": survey.status,
            "questions": survey.payload["questions"]
        },
        "responses": [
            {"id": r.id, "caller_id": r.caller_id, "answers": r.answers}
            for r in responses
        ]
    }