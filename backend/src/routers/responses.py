from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import Survey, SurveyResponse, SurveyAnswerItem
from ..schemas import SurveyAnswer

router = APIRouter(
    prefix="/responses",
    tags=["responses"]
)

# POST /responses/create
@router.post("/create", status_code=201)
def create_response(payload: SurveyAnswer, session: Session = Depends(get_session)):
    survey = session.get(Survey, payload.survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    response = SurveyResponse(
        survey_id=payload.survey_id,
        session_id=payload.session_id
    )
    session.add(response)
    session.commit()
    session.refresh(response)

    for item in payload.answers:
        answer_item = SurveyAnswerItem(
            response_id=response.id,
            question_id=item.question_id,
            response=str(item.response)
        )
        session.add(answer_item)

    session.commit()
    return {"status": "ok", "response_id": response.id}

# GET /responses/list/{survey_id}
@router.get("/list/{survey_id}")
def list_responses(survey_id: int, session: Session = Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    responses = session.exec(
        select(SurveyResponse).where(SurveyResponse.survey_id == survey_id)
    ).all()

    result = []
    for r in responses:
        items = session.exec(
            select(SurveyAnswerItem).where(SurveyAnswerItem.response_id == r.id)
        ).all()

        result.append({
            "session_id": r.session_id,
            "answers": [
                {"question_id": it.question_id, "response": it.response}
                for it in items
            ]
        })

    return {"survey_id": survey_id, "responses": result}

# GET /responses/details/{response_id}
@router.get("/details/{response_id}")
def response_details(response_id: int, session: Session = Depends(get_session)):
    response = session.get(SurveyResponse, response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")

    items = session.exec(
        select(SurveyAnswerItem).where(SurveyAnswerItem.response_id == response_id)
    ).all()

    return {
        "response_id": response_id,
        "session_id": response.session_id,
        "survey_id": response.survey_id,
        "answers": [
            {"question_id": it.question_id, "response": it.response}
            for it in items
        ]
    }