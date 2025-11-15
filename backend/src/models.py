from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str
    password_hash: str
    full_name: str

    organization_type: str
    organization_id: str

    is_email_verified: bool = False
    is_active: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)

    surveys: List["Survey"] = Relationship(back_populates="user")


class Survey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="surveys")

    questions: List["Question"] = Relationship(back_populates="survey")
    responses: List["SurveyResponse"] = Relationship(back_populates="survey")


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    survey_id: int = Field(foreign_key="survey.id")
    type: str
    text: str
    required: bool = False

    # stored as JSON text
    options: Optional[str] = None

    survey: Optional[Survey] = Relationship(back_populates="questions")


class SurveyResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    survey_id: int = Field(foreign_key="survey.id")
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    survey: Optional[Survey] = Relationship(back_populates="responses")
    answer_items: List["SurveyAnswerItem"] = Relationship(back_populates="response")


class SurveyAnswerItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    response_id: int = Field(foreign_key="surveyresponse.id")
    question_id: int
    response: str

    response: Optional[SurveyResponse] = Relationship(back_populates="answer_items")