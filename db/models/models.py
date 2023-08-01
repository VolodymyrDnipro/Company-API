from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Enum, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PyEnum
from db.session import metadata

Base = declarative_base(metadata=metadata)


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    frequency_in_days = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with Company model
    company = relationship("Company", back_populates="quizzes")
    # Relationship with Question model
    questions = relationship("Question", back_populates="quiz")
    # Relationship with User model
    user = relationship("User", back_populates="quizzes")
    # Relationship with QuizResult model
    quiz_results = relationship("QuizResult", back_populates="quiz")


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    question_text = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with Quiz model
    quiz = relationship("Quiz", back_populates="questions")
    # Relationship with Answer model
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    # Relationship with Question model
    question = relationship("Question", back_populates="answers")


class QuizResult(Base):
    __tablename__ = 'quiz_results'

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship with User model
    user = relationship("User", back_populates="quiz_results")
    # Relationship with Quiz model
    quiz = relationship("Quiz", back_populates="quiz_results")


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
    # Relationship with Quiz model
    quizzes = relationship("Quiz", back_populates="company")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    average_score = Column(Float, default=0.0)

    # Relationship with Company model
    companies = relationship("Company", back_populates="owner")
    # Relationship with CompanyRequest model
    user_requests = relationship("CompanyRequest", back_populates="user")
    # Relationship with CompanyRole model
    user_roles = relationship("CompanyRole", back_populates="user")
    # Relationship with QuizResult model
    quiz_results = relationship("QuizResult", back_populates="user")
    # Relationship with Quiz model
    quizzes = relationship("Quiz", back_populates="user")
