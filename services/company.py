from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import User, Company
from schemas.company import CompanyCreate, UpdateCompanyRequest
from managers.base_manager import CRUDBase


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.company_crud = CRUDBase[Company](Company, session)
        self.user_crud = CRUDBase[User](User, session)

    async def get_all_companies(self) -> List[Company]:
        return await self.company_crud.get_all()

    async def get_company_by_id(self, company_id: int) -> Company:
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        return company

    async def create_company(self, company_data: CompanyCreate, email: str) -> Company:
        user = await self.user_crud.get_by_field(email, field_name='email')
        company = Company(name=company_data.name, description=company_data.description,
                          visibility=company_data.visibility,
                          owner_id=user.user_id)
        created_company = await self.company_crud.create(company)
        return created_company

    async def update_company(self, company_data: UpdateCompanyRequest, company_id: int,
                             email: str) -> Company:
        user = await self.user_crud.get_by_field(email, field_name='email')
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if user.user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        updated_company = await self.company_crud.update(company, company_data.dict())
        return updated_company

    async def delete_company(self, company_id: int, email: str) -> None:
        user = await self.user_crud.get_by_field(email, field_name='email')
        company = await self.company_crud.get_by_field(company_id, field_name='company_id')
        if user.user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        deleted_company = await self.company_crud.delete(company)
        return deleted_company
