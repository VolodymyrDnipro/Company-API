from typing import List

from fastapi import HTTPException
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import (Answer, Company, User, CompanyMembership, CompanyRequest, CompanyRole, Quiz, QuizResult,
                              Question, UserAnswers)
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

    async def find_users_results_by_user_id(self, user_id: int) -> List[QuizResult]:
        return await self.quiz_result_crud.get_all(user_id=user_id)

    async def find_user_result_by_user_id(self, user_id: int) -> QuizResult:
        return await self.quiz_result_crud.get_by_field(user_id, field_name="user_id")

    async def get_self_rating(self, user_email: str) -> int:
        user = await self.find_auth_user_by_email(user_email)
        user_rating = user.average_score
        return user_rating

    async def get_user_rating_by_all_quizzes_by_date(self, user_email: str, start_date: date, end_date: date) -> List[dict]:
        user = await self.find_auth_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        quiz_results = await self.find_users_results_by_user_id(user.user_id)
        if not quiz_results:
            raise HTTPException(status_code=404, detail="No quiz found")

        filtered_results = [result for result in quiz_results if start_date <= result.timestamp.date() <= end_date]

        unique_quiz_ids = set(result.quiz_id for result in filtered_results)

        average_scores = []

        for quiz_id in unique_quiz_ids:
            true_count = sum(result.result for result in filtered_results if result.quiz_id == quiz_id)
            average_scores.append({"quiz": quiz_id, "average_count": true_count})

        return average_scores

    async def get_quizzes_and_last_completion_time(self, user_email: str) -> List[dict]:
        user = await self.find_auth_user_by_email(user_email)
        quizzes = await self.find_users_results_by_user_id(user_id=user.user_id)
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
            quiz_results = await self.find_users_results_by_user_id(user_id)
            if not quiz_results:
                continue

            filtered_results = [result for result in quiz_results if start_date <= result.timestamp.date() <= end_date]

            true_count = sum(result.result for result in filtered_results)

            average_scores.append({"user": user_id, "average_count": true_count})

        return average_scores


    async def company_get_average_scores_by_user_id(self, user_id: int, company_id: int, start_date: date, end_date: date) -> List[dict]:
        user = await self.find_user_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        # check user in company
        company_member = await self.find_user_in_company(company_id, user_id)
        if not company_member:
            raise HTTPException(status_code=404, detail="No user found in company")

        quiz_results = await self.find_users_results_by_user_id(user.user_id)
        if not quiz_results:
            raise HTTPException(status_code=404, detail="No quiz found")

        filtered_results = [result for result in quiz_results if start_date <= result.timestamp.date() <= end_date]

        unique_quiz_ids = set(result.quiz_id for result in filtered_results)

        average_scores = []

        for quiz_id in unique_quiz_ids:
            true_count = sum(result.result for result in filtered_results if result.quiz_id == quiz_id)
            average_scores.append({"quiz": quiz_id, "average_count": true_count})

        return average_scores

    async def company_get_all_users_and_last_completion_time(self, company_id: int) -> List[dict]:
        company_members = await self.find_all_company_members_by_company_id(company_id)

        user_completion_times = {}

        for member in company_members:
            users_results = await self.find_users_results_by_user_id(user_id=member.user_id)
            if not users_results:
                continue
            last_completion_time = max(result.timestamp for result in users_results)
            user_completion_times[member.user_id] = last_completion_time

        result = [{"user_id": user_id, "last_completion_time": timestamp.isoformat()} for user_id, timestamp in
                  user_completion_times.items()]
        return result






