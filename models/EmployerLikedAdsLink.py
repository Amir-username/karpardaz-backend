from typing import Optional
from sqlmodel import SQLModel, Field


class EmployerLikedAdsLink(SQLModel, table=True):
    employer_id: Optional[int] = Field(
        default=None, foreign_key="employerdetail.id", primary_key=True
    )
    advertisement_id: Optional[int] = Field(
        default=None, foreign_key="jobseekerad.id", primary_key=True
    )