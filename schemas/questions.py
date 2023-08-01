from typing import List, Optional
from pydantic import BaseModel, field_validator
from .answers import AnswerCreate, AnswerUpdate


class QuestionBase(BaseModel):
    question_id: int
    quiz_id: int
    question_text: str
    is_active: bool


class QuestionCreate(BaseModel):
    question_text: str
    is_active: bool
    answers: List[AnswerCreate]

    @field_validator("answers")
    def check_minimum_answers(cls, answers):
        if len(answers) < 2:
            raise ValueError("Each question must have at least two answer options")
        return answers


class QuestionUpdate(BaseModel):
    question_text: Optional[str]
    is_active: Optional[bool]
