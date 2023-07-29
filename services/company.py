from fastapi import HTTPException, status
from typing import List, Dict

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import User, Company, CompanyMembership, CompanyRequest, RequestStatus, RequestCreatedBy, CompanyRole, RoleType
from schemas.company import CompanyCreate, UpdateCompany, UpdateCompanyRequest, UpdateCompanyMembershipRequest, \
    UserLeaveCompanyRequest
from managers.base_manager import CRUDBase


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.company_crud = CRUDBase[Company](Company, session)
        self.user_crud = CRUDBase[User](User, session)
        self.membership_crud = CRUDBase[CompanyMembership](CompanyMembership, session)
        self.company_request_crud = CRUDBase[CompanyRequest](CompanyRequest, session)
        self.company_role_crud = CRUDBase[CompanyRole](CompanyRole, session)

    async def get_all_companies(self) -> List[Company]:
        return await self.company_crud.get_all()

    async def get_company_by_id(self, company_id: int) -> Company:
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        return company

    # # BLOCK OWNER # #
    async def create_company(self, company_data: CompanyCreate, email: str) -> Company:
        # Знаходимо юзера
        user = await self.user_crud.get_by_field(email, field_name='email')
        # Створюємо компанію
        company = Company(name=company_data.name, description=company_data.description,
                          visibility=company_data.visibility,
                          owner_id=user.user_id)
        created_company = await self.company_crud.create(company)
        # Додаємо Овнера до таблиці CompanyMembership як Овнера
        company_member = CompanyMembership(user_id=user.user_id, company_id=created_company.company_id, is_owner=True)
        await self.membership_crud.create(company_member)
        company_role = CompanyRole(user_id=user.user_id, company_id= created_company.company_id, role_type=RoleType.OWNER)
        await self.company_role_crud.create(company_role)
        return created_company

    async def update_company(self, company_data: UpdateCompany, company_id: int,
                             email: str) -> Company:
        # Знаходимо юзера
        user = await self.user_crud.get_by_field(email, field_name='email')
        # Знаходимо компанію
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if user.user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        updated_company = await self.company_crud.update(company, company_data.dict())
        return updated_company

    async def deactivate_company(self, company_id: int, email: str) -> Company:
        # find auth_user by email
        user = await self.user_crud.get_by_field(email, field_name='email')

        # Знаходимо компанію
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if user.user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        # Оновлюємо поле is_active на False
        update_data = {'is_active': False}
        deactivated_company = await self.company_crud.update(company, update_data)

        return deactivated_company


    # # FIND WHO USER IN COMPANY # #
    async def check_who_this_user_in_company_admin_or_owner_by_company_id(self, email: str, company_id: int) -> None:
        # Find auth_user by email
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # Find company
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Not found company_id")

        # Find user role in company
        role_in_company = await self.company_role_crud.get_by_fields(user_id=auth_user.user_id,
                                                                     company_id=company.company_id)

        # Check role for company
        if role_in_company.role_type not in [RoleType.OWNER, RoleType.ADMIN]:
            raise HTTPException(status_code=403, detail="Forbidden to update")

    async def check_who_this_user_in_company_admin_or_owner_by_request_id(self, email: str, request_id: int) -> None:
        # Find auth_user by email
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # Find request if request_id is not None
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not request:
            raise HTTPException(status_code=404, detail="Not found request_id")

        # Find company using a request_id
        company = await self.company_crud.get_by_field(request.company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Not found company for the given request_id")

        # Find user role in company
        role_in_company = await self.company_role_crud.get_by_fields(user_id=auth_user.user_id,
                                                                     company_id=company.company_id)

        # Check role for company
        if role_in_company.role_type not in [RoleType.OWNER, RoleType.ADMIN]:
            raise HTTPException(status_code=403, detail="Forbidden to update")

    async def check_user_not_in_company_membership_by_user_id(self, company_id: int, user_id: int) -> None:
        # Find company
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Not found company_id")

        # Check user in company
        company_membership = await self.membership_crud.get_by_fields(user_id=user_id,
                                                                                  company_id=company.company_id)
        if company_membership:
            raise HTTPException(status_code=403,
                                detail="User with the provided user_id is already a member of this company")

    async def create_request_to_invite_from_company(self, company_id: int, user_id: int) -> CompanyRequest:
        # Компанією створюємо реквест для юзера із статусом PENDING
        new_request = CompanyRequest(user_id=user_id, company_id=company_id, created_by=RequestCreatedBy.COMPANY)
        await self.company_request_crud.create(new_request)

        return new_request

    # # Deactivated REQUEST # #
    async def company_deactivated_request_to_user(self, request_id: int) -> CompanyRequest:
        # find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not request:
            raise HTTPException(status_code=404, detail="Not found request")

        update_data = {'status': RequestStatus.DEACTIVATED}
        updated_request = await self.company_request_crud.update(request, update_data)

        return updated_request

    async def company_update_company_request(self, request_id: int, request_data: UpdateCompanyRequest) -> Company:
        # find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        # update request
        updated_company_request = await self.company_request_crud.update(request, request_data.dict())
        return updated_company_request

    async def check_user_in_company_by_request_id(self, request_id: int) -> None:
        # Find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not request:
            raise HTTPException(status_code=404, detail="Not found request")

        # Check if the user is already a member or has a pending request
        membership = await self.membership_crud.get_by_fields(user_id=request.user_id, company_id=request.company_id)
        if membership:
            raise HTTPException(status_code=409, detail="User is already a member of this company")

        # Check if the user already has a pending request for this company
        pending_request = await self.company_request_crud.get_by_fields(user_id=request.user_id,
                                                                        company_id=request.company_id,
                                                                        status=RequestStatus.PENDING)
        if pending_request:
            raise HTTPException(status_code=409, detail="User has a pending request for this company")

    async def accepted_or_declined_user_request(self, request_id: int, request_data: UpdateCompanyRequest) -> None:
        # Find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        # Update request
        await self.company_request_crud.update(request, request_data.dict())

    async def company_add_user_to_membership(self, request_id: int) -> None:
        # Find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        # add user to CompanyMembership
        company_member = CompanyMembership(user_id=request.user_id, company_id=request.company_id)
        await self.membership_crud.create(company_member)
        company_role = CompanyRole(user_id=request.user_id, company_id=request.company_id,
                                   role_type=RoleType.USER)
        await self.company_role_crud.create(company_role)

    async def get_all_request_from_company_to_users(self, company_id: int) -> List[CompanyRequest]:
        # get all request from company to users with status PENDING
        return await self.company_request_crud.get_all(company_id=company_id, created_by=RequestCreatedBy.COMPANY,
                                                       status=RequestStatus.PENDING)

    async def get_all_request_from_users_to_company(self, company_id: int) -> List[CompanyRequest]:
        # get all request from users to company with status PENDING
        return await self.company_request_crud.get_all(company_id=company_id, created_by=RequestCreatedBy.USER,
                                                       status=RequestStatus.PENDING)

    async def get_all_users_in_company_by_company_id(self, company_id: int) -> List[CompanyMembership]:
        # find company
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Not found company_id")
        # get all users in company
        return await self.membership_crud.get_all(company_id=company.company_id, is_active=True)

    async def check_user_in_company_membership(self, company_id: int, user_id: int) -> None:
        # find user
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user")
        # check user in CompanyMembership
        company_member = await self.membership_crud.get_by_fields(company_id=company_id, user_id=user_id)
        if not company_member:
            raise HTTPException(status_code=404, detail="Not found user in company")

    async def company_deactivate_user_from_membership(self, company_id: int, request_data: UpdateCompanyMembershipRequest) -> None:
        # find user in CompanyMembership table
        user_membership = await self.membership_crud.get_by_fields(company_id=company_id, user_id=request_data.user_id)

        # Check if the user is the owner of the company
        if user_membership.is_owner:
            raise HTTPException(status_code=403, detail="Forbidden: Cannot deactivate the owner of the company")

        await self.membership_crud.update(user_membership, request_data.dict())


    async def check_user_is_not_in_company_by_email(self, company_id: int, email: str) -> None:
        # Find auth_user by email
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # Find company
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Not found company_id")

        # Check user in company
        company_membership_via_email = await self.membership_crud.get_by_fields(user_id=auth_user.user_id,
                                                                                company_id=company.company_id)
        if company_membership_via_email:
            raise HTTPException(status_code=403, detail="You are already a member of this company")

    async def check_user_request_existence(self, company_id: int, email: str) -> None:
        # find auth_user by email
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # check user has request by this company
        try:
            company_request = await self.company_request_crud.get_by_fields(user_id=auth_user.user_id,
                                                                            company_id=company_id)
            if company_request and company_request.status in [RequestStatus.PENDING, RequestStatus.ACCEPTED]:
                raise HTTPException(status_code=403, detail="User is already a member or has a pending request")
        except NoResultFound:
            pass

    async def create_request_to_company_by_user(self, company_id: int, email: str) -> CompanyRequest:
        # find auth user
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # Check if company exists
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        # create request to company from user. Status = Pending
        new_request = CompanyRequest(user_id=auth_user.user_id, company_id=company_id, created_by=RequestCreatedBy.USER)
        await self.company_request_crud.create(new_request)

        return new_request

    async def check_user_can_cancel_request(self, request_id: int, email: str) -> None:
        # Find auth_user by email
        auth_user = await self.user_crud.get_by_field(email, field_name='email')

        # Find the request
        company_request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not company_request:
            raise HTTPException(status_code=404, detail="Request not found")

        # Check if the request status is "PENDING"
        if company_request.status != RequestStatus.PENDING:
            raise HTTPException(status_code=403, detail="Forbidden to cancel request")

        # Check if the user is the creator of the request
        if company_request.user_id != auth_user.user_id:
            raise HTTPException(status_code=403, detail="Forbidden to cancel request")

    async def cancel_user_request_to_company(self, request_id: int) -> CompanyRequest:
        # Find the request
        company_request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not company_request:
            raise HTTPException(status_code=404, detail="Request not found")

        # Update the request status to "DEACTIVATED"
        company_request.status = RequestStatus.DEACTIVATED
        updated_request = await self.company_request_crud.update(company_request, {'status': RequestStatus.DEACTIVATED})

        return updated_request

    async def check_that_user_created_request(self, request_id: int, email: str) -> None:
        # Find user
        user = await self.user_crud.get_by_field(email, field_name='email')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user_id")

        # Find request
        request = await self.company_request_crud.get_by_field(request_id, field_name='request_id')
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.user_id != user.user_id:
            raise HTTPException(status_code=403, detail="Forbidden: You are not the sender of this request")

        if request.status != RequestStatus.PENDING:
            raise HTTPException(status_code=403, detail="Forbidden: Request status cannot be updated")

    async def get_user_requests_by_email(self, email: str) -> List[CompanyRequest]:
        # Find user
        user = await self.user_crud.get_by_field(email, field_name='email')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user_id")

        return await self.company_request_crud.get_all(user_id=user.user_id, created_by=RequestCreatedBy.COMPANY,
                                                       status=RequestStatus.PENDING)

    async def get_user_created_requests_by_email(self, email: str) -> List[CompanyRequest]:
        # find user
        user = await self.user_crud.get_by_field(email, field_name='email')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user_id")

        return await self.company_request_crud.get_all(user_id=user.user_id, created_by=RequestCreatedBy.USER,
                                                       status=RequestStatus.PENDING)

    async def check_user_in_company_by_email(self, company_id: int, email: str) -> None:
        # find user
        user = await self.user_crud.get_by_field(email, field_name='email')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user")

        # check user in CompanyMembership
        company_member = await self.membership_crud.get_by_fields(company_id=company_id, user_id=user.user_id)
        if not company_member:
            raise HTTPException(status_code=404, detail="Not found user in company")

    async def user_leave_from_company(self, company_id: int, email: str, request_data: UserLeaveCompanyRequest) -> None:
        # find user
        user = await self.user_crud.get_by_field(email, field_name='email')
        if not user:
            raise HTTPException(status_code=404, detail="Not found user")
        # find user in CompanyMembership table
        user_membership = await self.membership_crud.get_by_fields(company_id=company_id, user_id=user.user_id)

        # Check if the user is the owner of the company
        if user_membership.is_owner:
            raise HTTPException(status_code=403, detail="Forbidden: The owner cannot leave the company")

        # Update user's is_active status
        await self.membership_crud.update(user_membership, request_data.dict())

