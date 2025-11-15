from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    organization_type: str
    organization_id: str
    
class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    id: int
    is_email_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
        
class QuestionBase(BaseModel):
    type: str
    text: str
    required: bool
    options: Optional[List[str]] = None
class QuestionCreate(QuestionBase):
    survey_id: int

class QuestionResponse(QuestionBase):
    id: int
    survey_id: int

    class Config:
        orm_mode = True

class SurveyBase(BaseModel):
    title: str
    description: str
class SurveyCreate(SurveyBase):
    questions: List[QuestionBase]
class SurveyResponse(SurveyBase):
    id: int
    created_at: datetime
    questions: List[QuestionResponse]
    class Config:
        orm_mode = True
class AnswerItem(BaseModel):
    question_id: int
    response: Any
class SurveyAnswer(BaseModel):
    survey_id: int
    session_id: str
    answers: List[AnswerItem]