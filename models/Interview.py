from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .Question import Question
    from .EmployerDetail import EmployerDetail
    from .JobSeekerDetail import JobSeekerDetail


class Interview(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    questions: List['Question'] = Relationship(back_populates='interview')
    employer_id: int | None = Field(
        foreign_key='employerdetail.id', ondelete='CASCADE')
    employer: 'EmployerDetail' = Relationship(back_populates='interview')
    jobseekers: List['JobSeekerDetail'] = Relationship(
        back_populates='interview')


'''
id
questions
employer
jobseekers
'''
