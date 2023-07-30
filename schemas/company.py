from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr
from db.models.models import CompanyVisibility, RequestStatus, RequestCreatedBy


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


# BLOCK COMPANY #

class ShowCompany(TunedModel):
    company_id: int
    name: str
    description: Optional[str]
    visibility: CompanyVisibility
    owner_id: int
    is_active: bool

    @classmethod
    def from_database(cls, db_model):
        return cls(
            company_id=db_model.company_id,
            name=db_model.name,
            description=db_model.description,
            visibility=db_model.visibility,
            owner_id=db_model.owner_id,
            is_active=db_model.is_active,
        )


class CompanyCreate(BaseModel):
    name: str = Field(..., description="Name of the company")
    description: Optional[str] = Field(None, description="Description of the company")
    visibility: CompanyVisibility = Field(
        CompanyVisibility.VISIBLE_TO_ALL,
        description="Visibility of the company"
    )


class UpdateCompany(BaseModel):
    name: Optional[constr(min_length=1)] = Field(None, description="Updated name of the user")
    description: Optional[constr(min_length=1)] = Field(None, description="Updated surname of the user")
    visibility: CompanyVisibility
    is_active: Optional[bool]


class UpdateCompanyResponse(BaseModel):
    updated_company_id: int


class DeleteCompanyResponse(BaseModel):
    deleted_company_id: int


# BLOCK COMPANY MEMBERSHIP #
class ShowCompanyMembership(TunedModel):
    user_id: int
    company_id: int
    is_owner: bool
    is_active: bool


class DeactivateCompanyMembershipResponse(TunedModel):
    user_id: int
    is_active: bool

class UserLeaveCompanyResponse(TunedModel):
    company_id: int
    is_active: bool

class UpdateCompanyMembershipRequest(BaseModel):
    user_id: int
    is_active: bool


class UserLeaveCompanyRequest(BaseModel):
    is_active: bool


# BLOCK COMPANY REQUEST #
class ShowCompanyRequest(TunedModel):
    request_id: int
    user_id: int
    company_id: int
    status: RequestStatus
    created_by: RequestCreatedBy

    @classmethod
    def from_database(cls, db_model):
        return cls(
            request_id=db_model.request_id,
            user_id=db_model.user_id,
            company_id=db_model.company_id,
            status=db_model.status,
            created_by=db_model.created_by,
        )


class DeactivatedCompanyRequestResponse(BaseModel):
    deactivated_request_id: int


class UpdateCompanyRequest(BaseModel):
    request_id: int
    status: RequestStatus


class UpdateCompanyRequestResponse(BaseModel):
    updated_request_id: int
    status: RequestStatus
