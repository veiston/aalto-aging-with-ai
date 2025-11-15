from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    type: str
    text: str
    options: Optional[List[str]] = None

class SurveyCreate(BaseModel):
    title: str
    questions: List[Question]

class SurveyOut(BaseModel):
    id: int
    title: str
    status: str
    payload: dict

    class Config:
        orm_mode = True

class ResponseIn(BaseModel):
    survey_id: int
    caller_id: str
    answers: List[str]

class ResponseOut(BaseModel):
    id: int
    caller_id: str
    answers: List[str]

    class Config:
        orm_mode = True