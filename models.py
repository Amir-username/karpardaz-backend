from sqlmodel import SQLModel, Field
from typing import Optional


class JobSeekerBase(SQLModel):
    firstname: str = Field(index=True)
    lastname: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    phonenumber: str = Field(unique=True)


class JobSeeker(JobSeekerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    avatar: str | None = None


class JobSeekerCreate(JobSeekerBase):
    password: str


class JobSeekerPublic(JobSeekerBase):
    id: int


class JobSeekerUpdate(SQLModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phonenumber: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None
