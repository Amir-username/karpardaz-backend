from typing import Optional
from sqlmodel import SQLModel, Field


class JobSeekerLikedAdsLink(SQLModel, table=True):
    jobseeker_id: Optional[int] = Field(
        default=None, foreign_key="jobseekerdetail.id", primary_key=True
    )
    advertisement_id: Optional[int] = Field(
        default=None, foreign_key="advertise.id", primary_key=True
    )