from sqlmodel import SQLModel, Field


class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=1, max_length=200)
    hashed_password: str = Field(nullable=False)