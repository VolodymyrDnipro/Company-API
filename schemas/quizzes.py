from typing import List, Optional
from pydantic import BaseModel, field_validator, constr, EmailStr, Field
from .questions import QuestionCreate, QuestionBase, QuestionUpdate
from .answers import AnswerBase


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True


# Pydantic schema for the Quiz model
class QuizBase(TunedModel):
    quiz_id: int
    company_id: int
    author_id: int
    name: str
    description: str
    frequency_in_days: int
    is_active: bool


class QuizCreate(BaseModel):
    company_id: int
    name: str
    description: str
    frequency_in_days: int
    is_active: bool
    questions: List[QuestionCreate]

    @field_validator("questions")
    def validate_questions(cls, questions: List[QuestionCreate]) -> List[QuestionCreate]:
        if len(questions) < 2:
            raise ValueError("Quiz must have at least two questions")
        return questions


class QuizUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    frequency_in_days: Optional[int]
    is_active: Optional[bool]


# Response Schemas

class AnswerResponse(AnswerBase):
    pass


class QuestionResponse(QuestionBase):
    pass


class QuizResponse(QuizBase):
    pass


class QuizResultResponse(TunedModel):
    result_id: int
    timestamp: str
