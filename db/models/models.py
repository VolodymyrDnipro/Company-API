from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Enum, Table
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PyEnum
from db.session import metadata

Base = declarative_base(metadata=metadata)


class CompanyMembership(Base):
    __tablename__ = 'company_membership'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'), primary_key=True)
    is_owner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class RequestStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    DEACTIVATED = "deactivated"


class RequestCreatedBy(PyEnum):
    USER = "user"
    COMPANY = "company"


class CompanyRequest(Base):
    __tablename__ = 'company_requests'

    request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    created_by = Column(Enum(RequestCreatedBy), default=RequestCreatedBy.USER)

    # Relationship with User model
    user = relationship("User", back_populates="user_requests")
    # Relationship with Company model
    company = relationship("Company", back_populates="company_requests")


class RoleType(PyEnum):
    OWNER = "owner"
    ADMIN = "admin"
    USER = "user"


class CompanyRole(Base):
    __tablename__ = 'company_roles'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    role_type = Column(Enum(RoleType), default=RoleType.USER)
    is_active = Column(Boolean, default=True)

    # Relationship with User model
    user = relationship("User", back_populates="user_roles")
    # Relationship with Company model
    company = relationship("Company", back_populates="company_roles")


class CompanyVisibility(PyEnum):
    HIDDEN = "hidden"
    VISIBLE_TO_ALL = "visible_to_all"


class Company(Base):
    __tablename__ = 'companies'

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(Enum(CompanyVisibility), default=CompanyVisibility.VISIBLE_TO_ALL)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with User model
    owner = relationship("User", back_populates="companies")
    # Relationship with CompanyRequest model
    company_requests = relationship("CompanyRequest", back_populates="company")
    # Relationship with CompanyRole model
    company_roles = relationship("CompanyRole", back_populates="company")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with Company model
    companies = relationship("Company", back_populates="owner")
    # Relationship with CompanyRequest model
    user_requests = relationship("CompanyRequest", back_populates="user")
    # Relationship with CompanyRole model
    user_roles = relationship("CompanyRole", back_populates="user")
