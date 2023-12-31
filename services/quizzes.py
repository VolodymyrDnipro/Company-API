from typing import Union, List

from fastapi import HTTPException
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
from services.notifications import NotificationsService


class QuizService:
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
        self.notifications_service = NotificationsService(session)

    async def find_auth_user_by_email(self, user_email: str) -> User:
        return await self.user_crud.get_by_field(user_email, field_name='email')

    async def find_user_by_user_id(self, user_id: int) -> User:
        return await self.user_crud.get_by_field(user_id, field_name='user_id')

    async def find_company_by_id(self, company_id: int) -> User:
        return await self.company_crud.get_by_field(company_id, field_name='company_id')

    async def get_quiz_by_quiz_id(self, quiz_id: int) -> Quiz:
        return await self.quizzes_crud.get_by_field(quiz_id, field_name='quiz_id')

    async def get_all_quizzes(self) -> List[Quiz]:
        return await self.quizzes_crud.get_all()

    async def get_all_company_quizzes(self, company_id: int) -> List[Quiz]:
        return await self.quizzes_crud.get_all(company_id=company_id, is_active=True)

    async def find_all_company_members(self) -> List[CompanyMembership]:
        return await self.membership_crud.get_all(is_active=True)

    async def find_all_company_members_by_company_id(self, company_id) -> List[CompanyMembership]:
        return await self.membership_crud.get_all(company_id=company_id, is_active=True)

    async def get_all_questions(self, quiz_id: int) -> List[Question]:
        return await self.question_crud.get_all(quiz_id=quiz_id)

    async def get_all_answer(self, question_id: int) -> List[Answer]:
        return await self.answers_crud.get_all(question_id=question_id)

    async def get_all_user_answers(self, user_id: int, quiz_id: int) -> List[UserAnswers]:
        return await self.user_answer_crud.get_all(user_id=user_id, quiz_id=quiz_id)

    async def get_question_by_question_id(self, question_id: int) -> Quiz:
        return await self.question_crud.get_by_field(question_id, field_name='question_id')

    async def get_answer_by_answer_id(self, answer_id: int) -> Quiz:
        return await self.answers_crud.get_by_field(answer_id, field_name='answer_id')

    async def get_quiz_result_by_id(self, result_id: int) -> Quiz:
        return await self.quiz_result_crud.get_by_field(result_id, field_name='result_id')

    async def create_quiz(self, user_email: str, quiz_data: QuizCreate) -> Quiz:
        auth_user = await self.find_auth_user_by_email(user_email)

        # We check whether a company with the specified company_id exists
        company = await self.find_company_by_id(quiz_data.company_id)
        if not company:
            raise HTTPException(status_code=404, detail="No company found")

        # Check if quiz_data.questions have at least two questions
        if len(quiz_data.questions) < 2:
            raise HTTPException(status_code=400, detail="Quiz must have at least two questions")

        created_quiz = Quiz(
            company_id=company.company_id,
            author_id=auth_user.user_id,
            name=quiz_data.name,
            description=quiz_data.description,
            frequency_in_days=quiz_data.frequency_in_days
        )

        # Insert the Quiz object to the database to generate the quiz_id
        await self.quizzes_crud.create(created_quiz)

        for question_data in quiz_data.questions:
            # Check if each question has at least two answers
            if len(question_data.answers) < 2:
                raise HTTPException(status_code=400, detail="Each question must have at least two answer options")

            question = Question(
                quiz_id=created_quiz.quiz_id,
                question_text=question_data.question_text,
                is_active=question_data.is_active
            )

            # Insert the Question object to the database to generate the question_id
            await self.question_crud.create(question)

            for answer_data in question_data.answers:
                answer = Answer(
                    quiz_id=created_quiz.quiz_id,
                    question_id=question.question_id,
                    answer_text=answer_data.answer_text,
                    is_correct=answer_data.is_correct
                )
                await self.answers_crud.create(answer)

        company_members = await self.find_all_company_members_by_company_id(company.company_id)
        for member in company_members:
            notification_text = f"New quiz '{created_quiz.quiz_id}' is available! Take the quiz now!"
            await self.notifications_service.create_notification(user_id=member.user_id, text=notification_text)

        return created_quiz

    async def update_quiz(self, quiz_id: int, quiz_data: QuizUpdate) -> Quiz:
        quiz = await self.get_quiz_by_quiz_id(quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="No quiz found")

        updated_quiz = await self.quizzes_crud.update(quiz, quiz_data.dict())
        return updated_quiz

    async def delete_quiz(self, quiz_id: int) -> Quiz:
        quiz = await self.get_quiz_by_quiz_id(quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="No quiz found")

        update_data = {'is_active': False}
        deleted_quiz = await self.quizzes_crud.update(quiz, update_data)
        return deleted_quiz

    async def update_question(self, question_id: int, question_data: QuestionUpdate) -> Quiz:
        question = await self.get_question_by_question_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="No question found")

        updated_question = await self.quizzes_crud.update(question, question_data.dict())
        return updated_question

    async def update_answer(self, answer_id: int, answer_data: AnswerUpdate) -> Quiz:
        answer = await self.get_answer_by_answer_id(answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="No answer found")

        updated_answer = await self.quizzes_crud.update(answer, answer_data.dict())
        return updated_answer

    async def create_user_answer(self, user_email: str, user_answer_data: UserAnswersCreate) -> UserAnswers:
        auth_user = await self.find_auth_user_by_email(user_email)
        if not auth_user:
            raise HTTPException(status_code=404, detail="No user found")

        quiz = await self.get_quiz_by_quiz_id(user_answer_data.quiz_id)

        questions = await self.get_all_questions(user_answer_data.quiz_id)
        if not questions:
            raise HTTPException(status_code=404, detail="No quiz found")

        all_user_answers = await self.user_answer_crud.get_all(user_id=auth_user.user_id)

        user_answers = [answer for answer in all_user_answers if
                        answer.question_id in [q.question_id for q in questions]]

        if any(answer.question_id == user_answer_data.question_id for answer in user_answers):

            if len(user_answers) == len(questions):

                last_answer = max(user_answers, key=lambda x: x.timestamp)

                if datetime.utcnow() - last_answer.timestamp < timedelta(days=quiz.frequency_in_days):
                    raise HTTPException(status_code=400,
                                        detail=f"You can start a new quiz process only after completing it {quiz.frequency_in_days} days")
            else:
                raise HTTPException(status_code=400, detail="This question has already been answered before")

        created_user_answer = await self.user_answer_crud.create(UserAnswers(
            user_id=auth_user.user_id,
            quiz_id=user_answer_data.quiz_id,
            question_id=user_answer_data.question_id,
            answer_id=user_answer_data.answer_id,
            timestamp=datetime.utcnow()
        ))

        return created_user_answer

    async def create_quiz_result(self, quiz_result_data: QuizResultCreate) -> List[QuizResult]:
        user = await self.find_user_by_user_id(quiz_result_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        quiz_results = []

        questions = await self.user_answer_crud.get_all(user_id=user.user_id)

        for question in questions:
            answers = await self.user_answer_crud.get_all(question_id=question.question_id)

            for answer in answers:
                quiz_data = await self.quizzes_crud.get_by_field(answer.quiz_id, field_name='quiz_id')

                question_data = await self.question_crud.get_by_field(question.question_id,
                                                                      field_name='question_id')

                answer_data = await self.answers_crud.get_by_field(answer.answer_id, field_name='answer_id')

                result = answer_data.is_correct

                quiz_result = QuizResult(
                    user_id=user.user_id,
                    quiz_id=quiz_data.quiz_id,
                    question_id=question_data.question_id,
                    user_answer_id=answer.user_answer_id,
                    result=result
                )
                quiz_results.append(quiz_result)
        for quiz_result in quiz_results:
            await self.quiz_result_crud.create(quiz_result)
        await self.calculate_and_update_average_score(user.user_id)
        await self.save_data_to_redis(user.user_id)
        return quiz_results

    async def calculate_and_update_average_score(self, user_id: int) -> int:
        quiz_results = await self.quiz_result_crud.get_all(user_id=user_id)

        true_count = sum(1 for quiz_result in quiz_results if quiz_result.result)

        user = await self.find_user_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        user_data = {"average_score": true_count}
        await self.user_crud.update(user, user_data)

        return true_count

    async def save_data_to_redis(self, user_id: int):
        redis_connection = await self.create_redis_connection()

        user = await self.find_user_by_user_id(user_id)
        company = await self.membership_crud.get_by_field(user.user_id, field_name='user_id')
        quiz_results = await self.quiz_result_crud.get_all(user_id=user.user_id)

        quiz_results_with_company = []
        for quiz_result in quiz_results:
            quiz_result_with_company = {
                'user_id': quiz_result.user_id,
                'quiz_id': quiz_result.quiz_id,
                'question_id': quiz_result.question_id,
                'user_answer_id': quiz_result.user_answer_id,
                'result': quiz_result.result,
                'company_id': company.company_id
            }
            quiz_results_with_company.append(quiz_result_with_company)

        quiz_results_json = json.dumps(quiz_results_with_company)
        await redis_connection.setex(str(user.user_id), 172800, quiz_results_json)
        redis_connection.close()

    async def create_redis_connection(self):
        redis_host = config.settings.REDIS_HOST
        redis_port = config.settings.REDIS_PORT

        redis_connection = await asyncio_redis.Connection.create(host=redis_host, port=redis_port)
        return redis_connection

    async def export_json_data_by_user_id(self, user_id: int):
        redis_connection = await self.create_redis_connection()

        data = await redis_connection.get(str(user_id))
        if not data:
            data_list = await self.quiz_result_crud.get_all(user_id=user_id)

            data_dict = {index: item for index, item in enumerate(data_list)}
            return data_dict

        data_dict = json.loads(data)
        return data_dict

    async def export_csv_data_by_user_id(self, user_id: int) -> Union[pd.DataFrame, dict]:
        redis_connection = await self.create_redis_connection()
        data = await redis_connection.get(str(user_id))
        if not data:
            data_list = await self.quiz_result_crud.get_all(user_id=user_id)
            data_dict = {index: item for index, item in enumerate(data_list)}
            return data_dict
        else:
            data_list = json.loads(data)
            data_frame = pd.DataFrame(data_list)
            return data_frame

    async def verification_of_belonging_to_one_company(self, user_email: str, user_id: int):
        auth_user = await self.find_auth_user_by_email(user_email)

        user = await self.find_user_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="No user found")

        company_user = await self.membership_crud.get_by_field(user_id, field_name='user_id')
        company_auth_user = await self.membership_crud.get_by_field(auth_user.user_id, field_name='user_id')
        if company_user.company_id != company_auth_user.company_id:
            raise HTTPException(status_code=403, detail="Forbidden download file")

    async def create_notifications(self):
        current_date = datetime.now()

        all_users = await self.find_all_company_members()

        for user in all_users:
            user_id = user.user_id
            company_id = user.company_id

            quizzes = await self.get_all_company_quizzes(company_id)

            for quiz in quizzes:
                quiz_id = quiz.quiz_id
                frequency = quiz.frequency_in_days

                questions = await self.get_all_questions(quiz_id)

                check_user_answers = await self.get_all_user_answers(user_id, quiz_id)

                if not check_user_answers:
                    notification_text = f"Quiz {quiz.name} is available! Take the test right now!"
                    await self.notifications_service.create_notification(user_id=user_id, text=notification_text)

                if len(check_user_answers) < len(questions):
                    notification_text = f"Complete the quiz {quiz.name}"
                    await self.notifications_service.create_notification(user_id=user_id, text=notification_text)

                if len(check_user_answers) == len(questions):
                    last_user_answer = None
                    max_timestamp = None

                    for answer in check_user_answers:
                        if max_timestamp is None or answer.timestamp > max_timestamp:
                            max_timestamp = answer.timestamp
                            last_user_answer = answer

                    if last_user_answer is not None and current_date - last_user_answer.timestamp >= timedelta(
                            days=frequency):
                        notification_text = f"The frequency in days {frequency} has already passed. Take the {quiz.name} test now!"
                        await self.notifications_service.create_notification(user_id=user_id, text=notification_text)
                    else:
                        continue
