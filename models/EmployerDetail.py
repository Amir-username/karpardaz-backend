from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from enum import Enum

if TYPE_CHECKING:
    from .Advertise import Advertise
    from .Employer import Employer


class PopulationEnum(str, Enum):
    SMALL = '۵ تا ۲۰ نفر'
    MEDIUM = '۲۰ تا ۵۰ نفر'
    LARGE = '۵۰ تا ۱۰۰ نفر'
    VERY_LARGE = '۱۰۰ نفر به بالا'


class EmployerDetailBase(SQLModel):
    address: str | None = Field(default=None)
    population: PopulationEnum | None = Field(default=PopulationEnum.SMALL)
    description: str | None = Field(default=None)
    avatar: str | None = Field(default=None)
    backdrop_image: str | None = Field(default=None)
    website: str | None = Field(default=None)


class EmployerDetailCreate(EmployerDetailBase):
    pass


class EmployerDetail(EmployerDetailBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employer_id: int | None = Field(default=None, foreign_key='employer.id')
    employer: 'Employer' = Relationship(back_populates='detail')
    company_name: str | None = Field(index=True, min_length=1, max_length=200, default=None)
    job_advertisements: List["Advertise"] | None = Relationship(
        back_populates="employer", cascade_delete=True)


class EmployerDetailUpdate(EmployerDetailBase):
    address: str | None = None
    population: PopulationEnum | None = None
    description: str | None = None
    avatar: str | None = None
    backdrop_image: str | None = None
    website: str | None = None
