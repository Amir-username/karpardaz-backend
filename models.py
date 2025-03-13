from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from passlib.context import CryptContext

import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class JobSeekerBase(SQLModel):
    firstname: str = Field(index=True, min_length=1, max_length=50)
    lastname: str = Field(index=True, min_length=1, max_length=50)
    email: EmailStr = Field(unique=True, index=True)
    phonenumber: str = Field(unique=True)

    @field_validator("phonenumber")
    def validate_phonenumber(cls, value):
        phone_regex = r"^(\+?98|0)9\d{9}$"
        if not re.match(phone_regex, value):
            raise ValueError("Phone number must be in a valid format")
        return value


class JobSeeker(JobSeekerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    avatar: str | None = None

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)


class JobSeekerCreate(JobSeekerBase):
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # if not any(char.isdigit() for char in value):
        #     raise ValueError("Password must contain at least one digit")
        # if not any(char.isupper() for char in value):
        #     raise ValueError("Password must contain at least one uppercase letter")
        # if not any(char.islower() for char in value):
        #     raise ValueError("Password must contain at least one lowercase letter")
        return value


class JobSeekerPublic(JobSeekerBase):
    id: int


class JobSeekerUpdate(SQLModel):
    firstname: str | None = Field(default=None, min_length=1, max_length=50)
    lastname: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
    password: str | None = None
    avatar: str | None = None
    phonenumber: str | None = None

    @field_validator("phonenumber")
    def validate_phonenumber(cls, value):
        phone_regex = r"^(\+?98|0)9\d{9}$"
        if not re.match(phone_regex, value):
            raise ValueError("Phone number must be in a valid format")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class EmployerBase(SQLModel):
    company_name: str = Field(index=True, min_length=1, max_length=200)
    email: EmailStr = Field(unique=True, index=True)


class Employer(EmployerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)


class EmployerCreate(EmployerBase):
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # if not any(char.isdigit() for char in value):
        #     raise ValueError("Password must contain at least one digit")
        # if not any(char.isupper() for char in value):
        #     raise ValueError("Password must contain at least one uppercase letter")
        # if not any(char.islower() for char in value):
        #     raise ValueError("Password must contain at least one lowercase letter")
        return value


class EmployerPublic(EmployerBase):
    id: int


class EmployerUpdate(SQLModel):
    company_name: str | None = Field(
        default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value
