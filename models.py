from sqlmodel import SQLModel, Field


class JobSeekerBase(SQLModel):
    firstname: str = Field(index=True)
    lastname: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    phonenumber: str = Field(unique=True)


class JobSeeker(JobSeekerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    avatar: str | None = None


class JobSeekerCreate(JobSeekerBase):
    password: str


class JobSeekerPublic(JobSeekerBase):
    id: int


class JobSeekerUpdate(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    password: str | None = None
    avatar: str | None = None
    phonenumber: str | None = None
