from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from ..Enums.status_enum import StatusEnum

if TYPE_CHECKING:
    from .JobSeekerDetail import JobSeekerDetail
    from .Advertise import Advertise


class AdRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None  = Field(default=None, foreign_key='jobseekerdetail.id')
    jobseeker: 'JobSeekerDetail' = Relationship(back_populates='requests')
    advertise_id: int | None  = Field(default=None, foreign_key='advertise.id')
    advertise: 'Advertise'= Relationship(back_populates='requests')
    status:  StatusEnum = Field(default=StatusEnum.PENDING)
