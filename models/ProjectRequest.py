from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .JobSeekerDetail import JobSeekerDetail
    from .Project import Project


class ProjectRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int | None = Field(
        foreign_key='project.id', ondelete='CASCADE')
    project: 'Project' = Relationship(back_populates='requests')
    jobseeker_id: int | None = Field(
        foreign_key='jobseekerdetail.id', ondelete='CASCADE')
    jobseeker: 'JobSeekerDetail' = Relationship(back_populates='requests')
