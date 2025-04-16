from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING, List
from ..Enums.experience_enum import ExperienceEnum

if TYPE_CHECKING:
    from .JobSeeker import JobSeeker
    from .JobSeekerAd import JobSeekerAd


class JobSeekerDetailBase(SQLModel):
    city: str = Field(max_length=50)
    educations: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=4
    )
    experiences: ExperienceEnum = ExperienceEnum.NO_EXPERIENSE
    avatar: str | None = Field(default=None)
    backdrop_image: str | None = Field(default=None)
    specialized_jobs: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=10
    )


class JobSeekerDetailCreate(JobSeekerDetailBase):
    pass


class JobSeekerDetail(JobSeekerDetailBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(default=None, foreign_key='jobseeker.id')
    jobseeker: 'JobSeeker' = Relationship(back_populates='detail')
    job_advertisements: List['JobSeekerAd'] | None = Relationship(
        back_populates="jobseeker", cascade_delete=True)


class JobSeekerDetailUpdate(JobSeekerDetailBase):
    city: str | None = None
    educations: List[str] | None = None
    experiences: ExperienceEnum | None = None
    avatar: str | None = None
    backdrop_image: str | None = None
    specialized_jobs: List[str] | None = None
