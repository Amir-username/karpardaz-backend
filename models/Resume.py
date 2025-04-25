from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .JobSeekerDetail import JobSeekerDetail


class ResumeBase(SQLModel):
    file_name: str = Field(..., min_length=1, max_length=400)
    file_data: bytes


class Resume(ResumeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(
        foreign_key='jobseekerdetail.id', ondelete='CASCADE')
    jobseeker: 'JobSeekerDetail' = Relationship(
        back_populates='resume')


class ResumeCreate(ResumeBase):
    ...


class ResumeUpdate(ResumeBase):
    file_name: str | None = None
    file_data: bytes | None = None
