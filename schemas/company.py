from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr
from db.models.models import CompanyVisibility



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

    @classmethod
    def from_database(cls, db_model):
        return cls(
            company_id=db_model.company_id,
            name=db_model.name,
            description=db_model.description,
            visibility=db_model.visibility,
            owner_id=db_model.owner_id,
        )


class CompanyCreate(BaseModel):
    name: str = Field(..., description="Name of the company")
    description: Optional[str] = Field(None, description="Description of the company")
    visibility: CompanyVisibility = Field(
        CompanyVisibility.VISIBLE_TO_ALL,
        description="Visibility of the company"
    )


class UpdateCompanyRequest(BaseModel):
    name: Optional[constr(min_length=1)] = Field(None, description="Updated name of the user")
    description: Optional[constr(min_length=1)] = Field(None, description="Updated surname of the user")
    visibility: CompanyVisibility


class UpdateCompanyResponse(BaseModel):
    updated_company_id: int


class DeleteCompanyResponse(BaseModel):
    deleted_company_id: int


# BLOCK COMPANY MEMBERSHIP #
class CompanyMembership(BaseModel):
    user_id: int
    company_id: int
    is_owner: bool

    class Config:
        from_attributes = True


class CompanyMembershipCreate(BaseModel):
    user_id: int
    is_owner: bool


class CompanyMembershipUpdate(BaseModel):
    is_owner: bool


class CompanyRequestBase(BaseModel):
    user_id: int
    company_id: int


class CompanyRequestCreate(CompanyRequestBase):
    pass


class CompanyRequestUpdate(CompanyRequestBase):
    status: str


class CompanyRequest(CompanyRequestBase):
    request_id: int
    status: str

    class Config:
        from_attributes = True


class CompanyRoleBase(BaseModel):
    user_id: int
    company_id: int


class CompanyRoleCreate(CompanyRoleBase):
    role_type: str


class CompanyRoleUpdate(CompanyRoleBase):
    role_type: str


class CompanyRole(CompanyRoleBase):
    role_id: int
    role_type: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    user_id: int
    companies: List[ShowCompany] = []
    requests: List[CompanyRequest] = []

    class Config:
        from_attributes = True


class UserWithCompanyRole(User):
    role_type: str

    class Config:
        from_attributes = True
