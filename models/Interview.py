from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, JSON
from pydantic import BaseModel


if TYPE_CHECKING:
    from .Advertise import Advertise


class Answer(BaseModel):
    jobseeker_id: int
    answers: list[str]


class Interview(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    questions: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )
    answers: Optional[List[Answer]] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )
    advertise_id: int | None = Field(
        foreign_key='advertise.id', ondelete='CASCADE')
    advertise: Optional['Advertise'] = Relationship(back_populates='interview')
    jobseeker_ids: Optional[List[int]] = Field(
        default_factory=list,
        sa_column=Column(JSON()),
    )
