from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from ..Enums.status_enum import StatusEnum

if TYPE_CHECKING:
    from .EmployerDetail import EmployerDetail
    from .JobSeekerAd import JobSeekerAd


class JobSeekerAdRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employer_id: int | None = Field(
        default=None, foreign_key='employerdetail.id')
    employer: 'EmployerDetail' = Relationship(back_populates='requests')
    advertise_id: int | None = Field(
        default=None, foreign_key='jobseekerad.id')
    advertise: 'JobSeekerAd' = Relationship(back_populates='requests')
    status:  StatusEnum = Field(default=StatusEnum.PENDING)
