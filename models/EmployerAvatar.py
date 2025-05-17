from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .EmployerDetail import EmployerDetail


class EmployerAvatarBase(SQLModel):
    file_name: str = Field(..., min_length=1, max_length=400,
                           description="Name of the image file")
    file_data: bytes = Field(..., description="Binary data of the image")


class EmployerAvatar(EmployerAvatarBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employer_id: int | None = Field(
        default=None,
        foreign_key="employerdetail.id",
        ondelete="CASCADE"
    )
    employer: Optional["EmployerDetail"] = Relationship(
        back_populates="avatar"
    )


class EmployerAvatarCreate(EmployerAvatarBase):
    pass


class EmployerAvatarUpdate(SQLModel):
    file_name: Optional[str] = Field(
        default=None, min_length=1, max_length=400)
    file_data: Optional[bytes] = None
