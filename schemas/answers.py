from typing import List, Optional
from pydantic import BaseModel, field_validator


class AnswerBase(BaseModel):
    answer_id: int
    question_id: int
    answer_text: str
    is_correct: bool


class AnswerCreate(BaseModel):
    answer_text: str
    is_correct: bool

    @field_validator("answer_text")
    def check_answer_text_length(cls, v):
        if not v.strip():
            raise ValueError("Answer text cannot be empty or contain only whitespace")
        return v


class AnswerUpdate(BaseModel):
    answer_text: Optional[str]
    is_correct: Optional[bool]

    @field_validator("answer_text")
    def check_answer_text_length(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Answer text cannot be empty or contain only whitespace")
        return v
