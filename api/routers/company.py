from fastapi import APIRouter, Depends, HTTPException, status, Body, Path, Query
from fastapi_pagination import Page, Params, paginate

from schemas.company import *
from services.company import CompanyService
from utils.dependencies import get_company_service
from utils.security import decode_bearer_token

company_router = APIRouter()


@company_router.get("/companies/", response_model=Page[ShowCompany])
async def get_companies(params: Params = Depends(),
                        company_service: CompanyService = Depends(get_company_service)):
    companies = await company_service.get_all_companies()
    if companies is None:
        raise HTTPException(status_code=404, detail="Companies not found")
    return paginate(companies, params)


@company_router.get("/company/{company_id}/", response_model=ShowCompany)
async def get_company(company_id: int = Path(...), company_service: CompanyService = Depends(get_company_service)):
    company = await company_service.get_company_by_id(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@company_router.post("/company/", response_model=ShowCompany)
async def create_company(company: CompanyCreate = Body(...), user_data: dict = Depends(decode_bearer_token),
                         company_service: CompanyService = Depends(get_company_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    created_company = await company_service.create_company(company, email)
    show_company = ShowCompany.from_database(created_company)
    return show_company


@company_router.put("/companies/{company_id}/", response_model=UpdateCompanyResponse)
async def update_company(company_id: int = Path(...), company: UpdateCompanyRequest = Body(...),
                         user_data: dict = Depends(decode_bearer_token),
                         company_service: CompanyService = Depends(get_company_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    updated_company = await company_service.update_company(company, company_id, email)
    return {"updated_company_id": updated_company.company_id}


@company_router.delete("/companies/{company_id}/", response_model=DeleteCompanyResponse)
async def delete_company(company_id: int = Path(...), user_data: dict = Depends(decode_bearer_token),
                         company_service: CompanyService = Depends(get_company_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    await company_service.delete_company(company_id, email)
    return {"deleted_company_id": company_id}



# @app.post("/users/", response_model=User)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     # Реалізація логіки створення користувача (додавання до бази даних)
#     # ...
#
#
# @app.put("/users/{user_id}/", response_model=User)
# def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     # Реалізація логіки оновлення користувача (зміна інформації в базі даних)
#     # ...
#
#
# @app.delete("/users/{user_id}/", response_model=User)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки видалення користувача (видалення з бази даних)
#     # ...
#
#
# @app.get("/users/", response_model=List[User])
# def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     # Реалізація логіки отримання списку користувачів з пагінацією (запит до бази даних)
#     # ...
#
#
# @app.get("/users/{user_id}/", response_model=User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки отримання конкретного користувача (запит до бази даних)
#     # ...
#
#
# # Роути для взаємодії з учасниками компаній та запитами на вступ до компаній
# @app.post("/company_membership/", response_model=CompanyMembership)
# def create_company_membership(membership: CompanyMembershipCreate, db: Session = Depends(get_db)):
#     # Реалізація логіки створення учасника компанії (додавання до бази даних)
#     # ...
#
#
# @app.put("/company_membership/{user_id}/", response_model=CompanyMembership)
# def update_company_membership(user_id: int, membership: CompanyMembershipUpdate, db: Session = Depends(get_db)):
#     # Реалізація логіки оновлення учасника компанії (зміна інформації в базі даних)
#     # ...
#
#
# @app.delete("/company_membership/{user_id}/", response_model=CompanyMembership)
# def delete_company_membership(user_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки видалення учасника компанії (видалення з бази даних)
#     # ...
#
#
# @app.get("/company_membership/{user_id}/", response_model=List[Company])
# def get_companies_by_user(user_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки отримання списку компаній, до яких належить користувач (запит до бази даних)
#     # ...
#
#
# @app.post("/company_requests/", response_model=CompanyRequest)
# def create_company_request(request: CompanyRequestCreate, db: Session = Depends(get_db)):
#     # Реалізація логіки створення запиту на вступ до компанії (додавання до бази даних)
#     # ...
#
#
# @app.put("/company_requests/{request_id}/", response_model=CompanyRequest)
# def update_company_request(request_id: int, request: CompanyRequestUpdate, db: Session = Depends(get_db)):
#     # Реалізація логіки оновлення статусу запиту на вступ до компанії (зміна статусу в базі даних)
#     # ...
#
#
# @app.delete("/company_requests/{request_id}/", response_model=CompanyRequest)
# def delete_company_request(request_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки відміни запиту на вступ до компанії (видалення з бази даних)
#     # ...
#
#
# @app.get("/company_requests/", response_model=List[CompanyRequest])
# def get_company_requests_by_user(user_id: int, db: Session = Depends(get_db)):
#     # Реалізація логіки отримання списку запитів на вступ до компаній користувача (запит до бази даних)
#     # ...
#
#     @app.get("/company_admins/{company_id}/", response_model=List[User])
#     def get_company_admins(company_id: int, db: Session = Depends(get_db)):
# # Реалізація логіки отримання списку адміністраторів компанії (запит до бази даних)
# # ...
