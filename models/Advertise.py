from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING
from ..Enums.position_enum import PositionEnum
from ..Enums.experience_enum import ExperienceEnum
from ..Enums.gender_enum import GenderEnum
from ..Enums.salary_enum import SalaryEnum

if TYPE_CHECKING:
    from .EmployerDetail import EmployerDetail


class AdvertiseBase(SQLModel):
    title: str = Field(..., min_length=1, max_length=200)
    position: PositionEnum
    experience: ExperienceEnum = ExperienceEnum.NO_EXPERIENSE
    salary: SalaryEnum = SalaryEnum.NEGOTIATED
    job_group: str = Field(..., max_length=100)
    city: str = Field(..., max_length=50)
    is_remote: bool
    is_internship: bool
    gender: GenderEnum = GenderEnum.NO_DIFFERENCE
    benefits: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=10  # Example max items
    )
    technologies: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=6
    )
    is_portfolio: bool
    description: str = Field(..., min_length=10, max_length=3000)


class Advertise(AdvertiseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employer_id: int | None = Field(foreign_key="employerdetail.id", ondelete="CASCADE")
    employer: "EmployerDetail" = Relationship(back_populates="job_advertisements")


class AdvertiseCreate(AdvertiseBase):
    pass


class AdvertisePublic(AdvertiseBase):
    id: int
    employer_id: int | None = None


class AdvertiseUpdate(AdvertiseBase):
    title: str | None = Field(None, min_length=1, max_length=200)
    position: PositionEnum | None = None
    salary: SalaryEnum | None = None
    experience: ExperienceEnum | None = None
    job_group: str | None = Field(None, max_length=100)
    city: str | None = Field(None, max_length=50)
    is_remote: bool | None = None
    is_internship: bool | None = None
    gender: GenderEnum | None = None
    benefits: list[str] | None = Field(None, max_length=10)
    technologies: list[str] | None = Field(None, max_items=15)
    is_portfolio: bool | None = None
    description: str | None = Field(None, min_length=10, max_length=3000)
