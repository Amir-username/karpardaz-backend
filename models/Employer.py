from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, field_validator
import re
from ..password import verify_password
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .Advertise import Advertise


class EmployerBase(SQLModel):
    company_name: str = Field(index=True, min_length=1, max_length=200)
    email: EmailStr = Field(unique=True, index=True)


class Employer(EmployerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    job_advertisements: List["Advertise"] | None = Relationship(
        back_populates="employer", cascade_delete=True)

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
