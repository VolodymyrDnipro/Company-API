from fastapi import HTTPException, status
from typing import List, Dict

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import *
from schemas.company import *
from schemas.quizzes import *
from schemas.questions import *
from schemas.answers import *
from managers.base_manager import CRUDBase
from schemas.users import ShowUser


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

    async def find_auth_user_by_email(self, user_email: str) -> User:
        return await self.user_crud.get_by_field(user_email, field_name='email')

    async def find_company_by_id(self, company_id: int) -> User:
        return await self.company_crud.get_by_field(company_id, field_name='company_id')

    async def get_quiz_by_quiz_id(self, quiz_id: int) -> Quiz:
        return await self.quizzes_crud.get_by_field(quiz_id, field_name='quiz_id')

    async def get_all_quizzes(self) -> List[Quiz]:
        return await self.quizzes_crud.get_all()

    async def get_question_by_question_id(self, question_id: int) -> Quiz:
        return await self.question_crud.get_by_field(question_id, field_name='question_id')

    async def get_answer_by_answer_id(self, answer_id: int) -> Quiz:
        return await self.answers_crud.get_by_field(answer_id, field_name='answer_id')

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

        for question_data in quiz_data.questions:
            # Check if each question has at least two answers
            if len(question_data.answers) < 2:
                raise HTTPException(status_code=400, detail="Each question must have at least two answer options")

            question = Question(
                quiz_id=created_quiz.quiz_id,
                question_text=question_data.question_text,
                is_active=question_data.is_active
            )

            created_answers = []
            for answer_data in question_data.answers:
                answer = Answer(
                    question_id=question.question_id,
                    answer_text=answer_data.answer_text,
                    is_correct=answer_data.is_correct
                )
                created_answers.append(answer)

            question.answers = created_answers
            created_quiz.questions.append(question)

        await self.quizzes_crud.create(created_quiz)

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
