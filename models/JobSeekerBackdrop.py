from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .JobSeekerDetail import JobSeekerDetail

class JobSeekerBackdropBase(SQLModel):
    file_name: str = Field(..., min_length=1, max_length=400, description="Name of the image file")
    file_data: bytes = Field(..., description="Binary data of the image")

class JobSeekerBackdrop(JobSeekerBackdropBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobseeker_id: int | None = Field(
        default=None,
        foreign_key="jobseekerdetail.id",
        ondelete="CASCADE"
    )
    jobseeker: Optional["JobSeekerDetail"] = Relationship(
        back_populates="backdrop_image"
    )

class JobSeekerBackdropCreate(JobSeekerBackdropBase):
    pass

class JobSeekerBackdropUpdate(SQLModel):
    file_name: Optional[str] = Field(default=None, min_length=1, max_length=400)
    file_data: Optional[bytes] = None
