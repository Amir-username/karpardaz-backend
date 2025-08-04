from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, field_validator
import re
from typing import TYPE_CHECKING
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



if TYPE_CHECKING:
    from core.password import verify_password
    from .JobSeekerDetail import JobSeekerDetail


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
    detail: 'JobSeekerDetail' = Relationship(back_populates='jobseeker')

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
