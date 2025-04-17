from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING
from ..Enums.position_enum import PositionEnum
from ..Enums.experience_enum import ExperienceEnum
from ..Enums.gender_enum import GenderEnum
from ..Enums.salary_enum import SalaryEnum

if TYPE_CHECKING:
    from .JobSeekerDetail import JobSeekerDetail


class JobSeekerAdBase(SQLModel):
    firstname: str = Field(index=True, min_length=1, max_length=50)
    lastname: str = Field(index=True, min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    position: PositionEnum = PositionEnum.JUNIOR
    experience: ExperienceEnum = ExperienceEnum.NO_EXPERIENSE
    salary: SalaryEnum = SalaryEnum.NEGOTIATED
    job_group: str = Field(..., max_length=100)
    is_remote: bool
    is_internship: bool
    gender: GenderEnum = GenderEnum.NO_DIFFERENCE
    technologies: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=6
    )
    is_portfolio: bool
    description: str = Field(..., min_length=10, max_length=3000)


class JobSeekerAdCreate(JobSeekerAdBase):
    ...


class JobSeekerAd(JobSeekerAdBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(
        foreign_key='jobseekerdetail.id', ondelete='CASCADE')
    jobseeker: 'JobSeekerDetail' = Relationship(
        back_populates='job_advertisements')


class JobSeekrAdUpdate(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    title: str | None = None
    position: PositionEnum | None = None
    experience: ExperienceEnum | None = None
    salary: SalaryEnum | None = None
    job_group: str | None = None
    is_remote: bool | None = None
    is_internship: bool | None = None
    gender: GenderEnum | None = None
    technologies: list[str] | None = None
    is_portfolio: bool | None = None
    description: str | None = None
