from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .JobSeeker import JobSeeker
    from .Advertise import Advertise


class JobSeekerDetailBase(SQLModel):
    city: str = Field(max_length=50)
    educations: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )
    experiences: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )
    avatar: str | None = Field(default=None)
    backdrop_image: str | None = Field(default=None)
    specialized_jobs: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )


class JobSeekerDetailCreate(JobSeekerDetailBase):
    pass


class JobSeekerDetail(JobSeekerDetailBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(default=None, foreign_key='jobseeker.id')
    jobseeker: 'JobSeeker' = Relationship(back_populates='detail')
    liked_advertisements: List['Advertise'] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )


class JobSeekerDetailUpdate(JobSeekerDetailBase):
    city: str | None = None
    educations: List[str] | None = None
    experiences: List[str] | None = None
    avatar: str | None = None
    backdrop_image: str | None = None
    specialized_jobs: List[str] | None = None
