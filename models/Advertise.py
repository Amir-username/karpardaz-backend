from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from enum import Enum
from sqlalchemy import Column, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Employer import Employer


# Enums for restricted choice fields
class PositionEnum(str, Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    MIDLEVEL = "midlevel"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Advertise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    employer_id: int = Field(foreign_key="employer.id")
    employer: "Employer" = Relationship(back_populates="job_advertisements")
    position: PositionEnum
    is_experience: bool
    job_group: str
    city: str
    is_remote: bool
    is_internship: bool
    gender: GenderEnum
    benefits: List[str] = Field(default_factory=list, sa_column=Column(JSON()))
    technologies: List[str] = Field(
        default_factory=list, sa_column=Column(JSON()))
    is_portfolio: bool
    description: str
