from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/ar4u")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/responses")
def receive_response(payload: schemas.ResponseIn, db: Session = Depends(get_db)):
    response = models.Response(
        survey_id=payload.survey_id,
        caller_id=payload.caller_id,
        answers=payload.answers
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return {"status": "ok", "id": response.id}