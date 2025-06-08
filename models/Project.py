from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .ProjectRequest import ProjectRequest
    from .EmployerDetail import EmployerDetail


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str = Field(..., min_length=10, max_length=3000)
    employer_id: int | None = Field(
        foreign_key='employerdetail.id', ondelete='CASCADE')
    employer: 'EmployerDetail' = Relationship(back_populates='projects')
    requests: List['ProjectRequest'] = Relationship(
        back_populates='project')
