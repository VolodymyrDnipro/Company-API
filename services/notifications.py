from typing import List

from fastapi import HTTPException
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import (Answer, Company, User, CompanyMembership, CompanyRequest, CompanyRole, Quiz, QuizResult,
                              Question, UserAnswers, Notification)
from managers.base_manager import CRUDBase

class NotificationsService:
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
        self.notification_crud = CRUDBase[Notification](Notification, session)

    async def find_auth_user_by_email(self, user_email: str) -> User:
        return await self.user_crud.get_by_field(user_email, field_name='email')

    async def find_user_notification_by_id(self, user_id: int, notification_id: int) -> Notification:
        return await self.notification_crud.get_by_fields(user_id=user_id, notification_id=notification_id)

    async def create_notification(self, user_id: int, text: str) -> Notification:
        notification = Notification(user_id=user_id, text=text)
        notification_created = await self.notification_crud.create(notification)
        return notification_created

    async def user_get_active_notifications_by_email(self, email: str) -> List[Notification]:
        auth_user = await self.find_auth_user_by_email(email)
        notifications = await self.notification_crud.get_all(user_id=auth_user.user_id, status=True)
        if not notifications:
            raise HTTPException(status_code=404, detail="No notifications found")
        return notifications

    async def user_mark_notification_as_read(self, email: str, notification_id: int) -> Notification:
        auth_user = await self.find_auth_user_by_email(email)

        notification = await self.find_user_notification_by_id(auth_user.user_id, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="No notification found")

        update_data = {'status': False}
        deactivated_notification = await self.notification_crud.update(notification, update_data)
        return deactivated_notification
