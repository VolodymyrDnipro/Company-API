from typing import List, Optional
from pydantic import BaseModel, field_validator, constr, EmailStr, Field
from .questions import QuestionCreate, QuestionBase, QuestionUpdate
from .answers import AnswerBase
from datetime import datetime


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


# # # QUIZ RESULT # # #
class QuizResultBase(TunedModel):
    result_id: int
    user_id: int
    quiz_id: int
    question_id: int
    user_answer_id: int
    result: bool


class QuizResultCreate(BaseModel):
    user_id: int


# # # USER ANSWERS # # #
class UserAnswersBase(BaseModel):
    user_answer_id: int
    user_id: int
    quiz_id: int
    question_id: int
    answer_id: int
    timestamp: datetime


class UserAnswersCreate(BaseModel):
    quiz_id: int
    question_id: int
    answer_id: int


# Response Schemas

class AnswerResponse(AnswerBase):
    pass


class QuestionResponse(QuestionBase):
    pass


class QuizResponse(QuizBase):
    pass


class QuizResultResponse(QuizResultBase):
    pass


class UserAnswersResponse(UserAnswersBase):
    pass

