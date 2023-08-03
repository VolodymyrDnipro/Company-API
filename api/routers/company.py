from fastapi import APIRouter, Depends, HTTPException, Body, Path
from fastapi_pagination import Page, Params, paginate

from schemas.company import (ShowCompany, CompanyCreate, UpdateCompany, UpdateCompanyResponse, ShowCompanyRequest,
                             DeactivatedCompanyRequestResponse, UpdateCompanyRequestResponse, UpdateCompanyRequest,
                             RequestStatus, ShowCompanyMembership, DeactivateCompanyMembershipResponse,
                             UpdateCompanyMembershipRequest, UserLeaveCompanyResponse, UserLeaveCompanyRequest,
                             UpdateCompanyRoleResponse, UpdateCompanyRoleRequest, RoleType)
from schemas.users import ShowUser
from services.company import CompanyService
from utils.dependencies import get_company_service
from api.routers.users import get_user_data

company_router = APIRouter()


@company_router.get("/companies/", response_model=Page[ShowCompany])
async def get_all_companies(params: Params = Depends(), user_email: str = Depends(get_user_data),
                            company_service: CompanyService = Depends(get_company_service)):
    companies = await company_service.get_all_companies()
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found")
    return paginate(companies, params)


@company_router.get("/company/{company_id}/", response_model=ShowCompany)
async def get_company(company_id: int = Path(...), user_email: str = Depends(get_user_data),
                      company_service: CompanyService = Depends(get_company_service)):
    company = await company_service.get_company_by_id(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@company_router.post("/company/", response_model=ShowCompany)
async def create_company(company: CompanyCreate = Body(...), user_email: str = Depends(get_user_data),
                         company_service: CompanyService = Depends(get_company_service)):
    created_company = await company_service.create_company(company, user_email)
    show_company = ShowCompany.from_database(created_company)
    return show_company


@company_router.put("/company/{company_id}/", response_model=UpdateCompanyResponse)
async def update_company(company_id: int = Path(...), company: UpdateCompany = Body(...),
                         user_email: str = Depends(get_user_data),
                         company_service: CompanyService = Depends(get_company_service)):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)
        # update company
        await company_service.update_company(company, company_id, user_email)
    except HTTPException as exc:
        raise exc
    return {"updated_company_id": company_id}


@company_router.delete("/deactivate_company/{company_id}/", response_model=UpdateCompanyResponse)
async def deactivate_company(company_id: int = Path(...),
                             user_email: str = Depends(get_user_data),
                             company_service: CompanyService = Depends(get_company_service)):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)
        # deactivate company
        await company_service.deactivate_company(company_id, user_email)
    except HTTPException as exc:
        raise exc
    return {"updated_company_id": company_id}


# Implementation of the logic of creating a request for an invite to the company by Ovner (adding to the data base)
@company_router.post("/company/{company_id}/request/{user_id}", response_model=ShowCompanyRequest)
async def create_request_to_user_from_company(
        company_id: int = Path(...),
        user_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)
        # check user is not in the company
        await company_service.check_user_not_in_company_membership_by_user_id(company_id, user_id)
        # create request on add to company
        new_request = await company_service.create_request_to_invite_from_company(company_id, user_id)
    except HTTPException as exc:
        raise exc

    return new_request

# Implementation of the logic of remote request to join the company (change the status to deactivated)
@company_router.put("/company/request/{request_id}/cancel/", response_model=DeactivatedCompanyRequestResponse)
async def company_cancel_request_to_user(
        request_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, request_id)
        # deactivated request
        await company_service.company_deactivated_request_to_user(request_id)
    except HTTPException as exc:
        raise exc

    return {"deactivated_request_id": request_id}


# Implementation of the logic of updating the request to join the company (changing the status to Accepted or Declined)
@company_router.put("/company_request/{request_id}/", response_model=UpdateCompanyRequestResponse)
async def company_update_user_request(
        request_data: UpdateCompanyRequest = Body(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        request_id = request_data.request_id
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_request_id(user_email, request_id)

        # check not company member create request
        await company_service.check_user_in_company_by_request_id(request_id)

        status = request_data.status

        if status == RequestStatus.DECLINED:
            # update on Declined
            await company_service.accepted_or_declined_user_request(request_id, request_data)
        else:
            # update on Accepted
            await company_service.accepted_or_declined_user_request(request_id, request_data)
            # add user to company_membership with role USER
            await company_service.company_add_user_to_membership(request_id)
    except HTTPException as exc:
        raise exc

    return {"updated_request_id": request_id, "status": request_data.status}


# Implementation of the logic of changing the Owner from the list of requests from the company to users
@company_router.get("/company_requests_from_company/{company_id}", response_model=Page[ShowCompanyRequest])
async def company_get_all_requests_from_company_to_users(
        params: Params = Depends(),
        company_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # get all request from company to users with status PENDING
        requests = await company_service.get_all_request_from_company_to_users(company_id)
    except HTTPException as exc:
        raise exc
    return paginate(requests, params)


# Implementation of the logic of taking the Owner from the list of requests from users to the company
@company_router.get("/company_requests_from_users/{company_id}", response_model=Page[ShowCompanyRequest])
async def company_get_all_requests_from_users_to_company(
        params: Params = Depends(),
        company_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # get all request from users to company with status PENDING
        requests = await company_service.get_all_request_from_users_to_company(company_id)
    except HTTPException as exc:
        raise exc
    return paginate(requests, params)


# Implementation of the visualization logic Users in company
@company_router.get("/company_get_all_users/{company_id}", response_model=Page[ShowCompanyMembership])
async def get_all_users_in_company(
        company_id: int = Path(...),
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # get all users in company
        users = await company_service.get_all_users_in_company_by_company_id(company_id)
    except HTTPException as exc:
        raise exc
    return paginate(users, params)


# Realization logic remote User from company
@company_router.put("/company_deactivate_user_in_company/{company_id}", response_model=DeactivateCompanyMembershipResponse)
async def company_deactivate_user_in_company(
        company_id: int = Path(...),
        request_data: UpdateCompanyMembershipRequest = Body(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        user_id = request_data.user_id
        is_active = request_data.is_active

        if not is_active:
            # check user in company
            await company_service.check_user_in_company_membership(company_id, user_id)
            # change user is_active = False
            await company_service.company_deactivate_user_from_membership(company_id, request_data)

    except HTTPException as exc:
        raise exc
    return {"user_id": user_id, "is_active": request_data.is_active}


# Implementation of the logic for creating a USER request for an invite to the company (adding to the data base)
@company_router.post("/user/{company_id}/request/", response_model=ShowCompanyRequest)
async def user_create_request_to_company(
        company_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check user is not in company
        await company_service.check_user_is_not_in_company_by_email(company_id, user_email)

        # check user doesn't have request
        await company_service.check_user_request_existence(company_id, user_email)

        # user create request to company
        new_request = await company_service.create_request_to_company_by_user(company_id, user_email)
    except HTTPException as exc:
        raise exc

    return new_request


# Implementation of the logic of remote access to the entry to the company by the User
@company_router.put("/user/request/{request_id}/cancel/", response_model=ShowCompanyRequest)
async def user_cancel_request_to_company(
        request_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # Check if the user can cancel the request
        await company_service.check_user_can_cancel_request(request_id, user_email)

        # Cancel the request (change status to "deactivated")
        canceled_request = await company_service.cancel_user_request_to_company(request_id)
    except HTTPException as exc:
        raise exc

    return canceled_request


# Implementation of the logic of updating the request for entry to the company by the User (changing the status to Accepted or Declined)
@company_router.put("/user/request/{request_id}/status/", response_model=UpdateCompanyRequestResponse)
async def user_update_company_request_status(
        request_data: UpdateCompanyRequest = Body(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        request_id = request_data.request_id
        # check the user that he created the request
        await company_service.check_that_user_created_request(request_id, user_email)

        # Check if the request status is valid
        if request_data.status not in [RequestStatus.ACCEPTED, RequestStatus.DECLINED]:
            raise HTTPException(status_code=400, detail="Invalid request status")

        status = request_data.status

        if status == RequestStatus.DECLINED:
            # update on Declined
            await company_service.accepted_or_declined_user_request(request_id, request_data)
        else:
            # update on Accepted
            await company_service.accepted_or_declined_user_request(request_id, request_data)
            # add user to company_membership with role USER
            await company_service.company_add_user_to_membership(request_id)
    except HTTPException as exc:
        raise exc

    return {"updated_request_id": request_id, "status": status}


# Implementation of the logic of ending the User to the list of requests for companies
@company_router.get("/user_requests/", response_model=Page[ShowCompanyRequest])
async def get_user_requests(
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # Getting all requests created by the company to users
        user_requests = await company_service.get_user_requests_by_email(user_email)
    except HTTPException as exc:
        raise exc
    return paginate(user_requests, params)


# Implementation of the logic of taking the User off the list of requests created by him to the company
@company_router.get("/user_created_requests/", response_model=Page[ShowCompanyRequest])
async def get_user_created_requests(
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # Get user-created requests
        user_requests = await company_service.get_user_created_requests_by_email(user_email)
    except HTTPException as exc:
        raise exc

    return paginate(user_requests, params)


@company_router.put("/users_leave_company/{company_id}", response_model=UserLeaveCompanyResponse)
async def user_leave_company(
        company_id: int = Path(...),
        request_data: UserLeaveCompanyRequest = Body(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # Check if the user is a member of the company
        await company_service.check_user_in_company_by_email(company_id, user_email)

        is_active = request_data.is_active

        if not is_active:
            # change user is_active = False
            await company_service.user_leave_from_company(company_id, user_email, request_data)

    except HTTPException as exc:
        raise exc
    return {"company_id": company_id, "is_active": request_data.is_active}


# Implementation of the logic change user role to the company
@company_router.put("/company/{company_id}/changed_user/{user_id}", response_model=UpdateCompanyRoleResponse)
async def company_change_user_role_in_company(
        company_id: int = Path(...),
        request_data: UpdateCompanyRoleRequest = Body(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # check user in company
        await company_service.check_user_in_company_membership(company_id, request_data.user_id)

        # change User Role
        await company_service.change_user_role_in_company(company_id, request_data)

    except HTTPException as exc:
        raise exc
    return {"user_id": request_data.user_id, "role_type": request_data.role_type}


# Implementation of the endpoint for removing the list of administrators from the company
@company_router.get("/company/{company_id}/company_members/{role_type}", response_model=Page[ShowUser])
async def get_company_admins(
        company_id: int = Path(...),
        role_type: RoleType = Path(...),
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service)
):
    try:
        # check auth user has owner or admin role
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # View the list of company administrators by id
        company_members = await company_service.get_all_members_in_company_by_role_type(company_id, role_type)
    except HTTPException as exc:
        raise exc

    return paginate(company_members, params)
