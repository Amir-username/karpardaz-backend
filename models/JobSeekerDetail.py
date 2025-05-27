from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING, List, Optional
from ..Enums.experience_enum import ExperienceEnum
from ..Enums.gender_enum import GenderEnum
from ..Enums.salary_enum import SalaryEnum
from ..Enums.position_enum import PositionEnum
from .JobSeekerLikedAdsLink import JobSeekerLikedAdsLink

if TYPE_CHECKING:
    from .JobSeeker import JobSeeker
    from .JobSeekerAd import JobSeekerAd
    from .Resume import Resume
    from .JobSeekerAvatar import JobSeekerAvatar
    from .Advertise import Advertise
    from .JobSeekerBackdrop import JobSeekerBackdrop
    from .AdRequest import AdRequest


class JobSeekerDetailBase(SQLModel):
    city: str = Field(max_length=50)
    educations: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=4
    )
    specialized_jobs: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
        max_items=10
    )

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
    portfolio_link: str | None = Field(default=None)
    description: str = Field(..., min_length=10, max_length=3000)


class JobSeekerDetailCreate(JobSeekerDetailBase):
    pass


class JobSeekerDetail(JobSeekerDetailBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(default=None, foreign_key='jobseeker.id')
    jobseeker: 'JobSeeker' = Relationship(back_populates='detail')
    job_advertisements: List['JobSeekerAd'] | None = Relationship(
        back_populates="jobseeker", cascade_delete=True)
    firstname: str | None = Field(
        default=None, index=True, min_length=1, max_length=50)
    lastname: str | None = Field(
        default=None, index=True, min_length=1, max_length=50)
    resume: Optional['Resume'] = Relationship(
        back_populates='jobseeker', cascade_delete=True)
    avatar: Optional['JobSeekerAvatar'] = Relationship(
        back_populates='jobseeker', cascade_delete=True)
    backdrop_image: Optional['JobSeekerBackdrop'] = Relationship(
        back_populates='jobseeker', cascade_delete=True)
    liked_advertisements: Optional[List['Advertise']] = Relationship(
        back_populates="jobseeker_likeds", link_model=JobSeekerLikedAdsLink)
    requests: Optional[List["AdRequest"]] = Relationship(
        back_populates="jobseeker")


class JobSeekerDetailUpdate(SQLModel):
    city: str | None = None
    educations: List[str] | None = None
    experiences: ExperienceEnum | None = None
    avatar: str | None = None
    backdrop_image: str | None = None
    specialized_jobs: List[str] | None = None
    position: PositionEnum | None = None
    salary: SalaryEnum | None = None
    job_group: str | None = None
    is_remote: bool | None = None
    is_internship: bool | None = None
    gender: GenderEnum | None = None
    technologies: list[str] | None = None
    is_portfolio: bool | None = None
    portfolio_link: str | None = None
    description: str | None = None
