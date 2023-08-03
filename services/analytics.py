from typing import Union, List

from fastapi import HTTPException, status
import json
from datetime import datetime, timedelta
import asyncio_redis
import config
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import (Answer, Company, User, CompanyMembership, CompanyRequest, CompanyRole, Quiz, QuizResult,
                              Question, UserAnswers)
from schemas.quizzes import QuizCreate, QuizUpdate, UserAnswersCreate, QuizResultCreate
from schemas.questions import QuestionUpdate
from schemas.answers import AnswerUpdate
from managers.base_manager import CRUDBase

class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.company_crud = CRUDBase[Company](Company, session)
        self.user_crud = CRUDBase[User](User, session)
        self.membership_crud = CRUDBase[CompanyMembership](CompanyMembership, session)
        self.company_request_crud = CRUDBase[CompanyRequest](CompanyRequest, session)
        self.company_role_crud = CRUDBase[CompanyRole](CompanyRole, session)
        self.quizzes_crud = CRUDBase[Quiz](Quiz, session)
        self.quiz_result_crud = CRUDBase[QuizResult](QuizResult, session)
        self.question_crud = CRUDBase[Question](Question, session)
        self.answers_crud = CRUDBase[Answer](Answer, session)
        self.user_answer_crud = CRUDBase[UserAnswers](UserAnswers, session)