from typing import Union, List

from fastapi import HTTPException, status
from datetime import date
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

    async def find_auth_user_by_email(self, user_email: str) -> User:
        return await self.user_crud.get_by_field(user_email, field_name='email')

    async def find_user_by_user_id(self, user_id: int) -> User:
        return await self.user_crud.get_by_field(user_id, field_name='user_id')

    async def find_company_by_company_id(self, company_id: int) -> Company:
        return await self.company_crud.get_by_field(company_id, field_name='company_id')

    async def find_all_company_members_by_company_id(self, company_id: int) -> List[CompanyMembership]:
        return await self.membership_crud.get_all(company_id=company_id)

    async def find_user_in_company(self, company_id: int, user_id: int) -> CompanyMembership:
        return await self.membership_crud.get_by_fields(company_id=company_id, user_id=user_id)

    async def find_user_result_by_user_id(self, user_id: int) -> List[QuizResult]:
        return await self.quiz_result_crud.get_all(user_id=user_id)

    async def find_user_results_by_user_id_and_date(self, user_id: int, start_date: date, end_date: date) -> List[QuizResult]:
        return await self.quiz_result_crud.get_all(user_id=user_id, timestamp__ge=start_date, timestamp__le=end_date)

    async def get_self_rating(self, user_email: str) -> int:
        user = await self.find_auth_user_by_email(user_email)
        user_rating = user.average_score
        return user_rating

    async def get_user_rating_by_all_quizzes_by_date(self, user_email: str, start_date: date, end_date: date) -> List[dict]:
        user = await self.find_auth_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        quiz_results = await self.find_user_results_by_user_id_and_date(user.user_id, start_date, end_date)
        if not quiz_results:
            raise HTTPException(status_code=404, detail="No quiz found")

        average_scores = []

        for quiz_result in quiz_results:
            quiz_id = quiz_result.quiz_id
            true_count = sum(1 for result in quiz_results if result.quiz_id == quiz_id and result.result)
            average_scores.append({"quiz": quiz_id, "average_count": true_count})

        return average_scores

    async def get_quizzes_and_last_completion_time(self, user_email: str) -> List[dict]:
        user = await self.find_auth_user_by_email(user_email)
        quizzes = await self.find_user_result_by_user_id(user_id=user.user_id)
        quiz_completion_times = {}

        for quiz in quizzes:
            quiz_id = quiz.quiz_id
            timestamp = quiz.timestamp
            if quiz_id in quiz_completion_times:
                quiz_completion_times[quiz_id] = max(quiz_completion_times[quiz_id], timestamp)
            else:
                quiz_completion_times[quiz_id] = timestamp

        result = [{"quiz_id": key, "last_completion_time": value} for key, value in quiz_completion_times.items()]
        return result

    async def company_get_average_scores(self, company_id: int, start_date: date, end_date: date) -> List[dict]:
        company_members = await self.find_all_company_members_by_company_id(company_id)
        average_scores = []

        for member in company_members:
            user_id = member.user_id
            quiz_results = await self.find_user_results_by_user_id_and_date(user_id, start_date, end_date)

            if not quiz_results:
                # No quiz found for the user, skip to the next member
                continue

            true_count = sum(1 for quiz_result in quiz_results if quiz_result.result)

            average_scores.append({"user": user_id, "average_count": true_count})

        return average_scores


    async def company_get_average_scores_by_all_users(self, user_id: int, company_id: int, start_date: date, end_date: date) -> List[dict]:
        user = await self.find_user_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        # check user in company
        company_member = await self.find_user_in_company(company_id, user_id)
        if not company_member:
            raise HTTPException(status_code=404, detail="No user found in company")

        quiz_results = await self.find_user_results_by_user_id_and_date(user_id, start_date, end_date)

        count_result_true = []

        result_true_count = sum(1 for quiz_result in quiz_results if quiz_result.result)

        count_result_true.append({"user": user_id, "average_count": result_true_count})

        return count_result_true

    async def company_get_all_users_and_last_completion_time(self, company_id: int) -> List[dict]:
        company_members = await self.find_all_company_members_by_company_id(company_id)

        user_last_completion_times = []

        for member in company_members:
            user_id = member.user_id
            last_completion_date = await self.quiz_result_crud.get_by_field(user_id, field_name="user_id")
            if last_completion_date:
                last_completion_date_str = last_completion_date.strftime("%Y-%m-%d %H:%M:%S")
                user_last_completion_times.append({"user": user_id, "last_date": last_completion_date_str})

        return user_last_completion_times




