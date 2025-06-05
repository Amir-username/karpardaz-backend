from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, JSON


if TYPE_CHECKING:
    from .Interview import Interview


class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    options: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON())
    )
    answer: str
    correct_answer: str
    interview_id: int | None = Field(
        foreign_key='interview.id', ondelete='CASCADE')
    interview: 'Interview' = Relationship(back_populates='questions')


'''
id
text
interview
options
answer
'''
