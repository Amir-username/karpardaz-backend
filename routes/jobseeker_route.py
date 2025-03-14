from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from ..auth.jobseeker_auth import authenticate_jobseeker
from ..auth.token import Token, create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

from ..models import JobSeeker, JobSeekerCreate, JobSeekerPublic, JobSeekerUpdate
from sqlmodel import Session, select
from ..session.session import get_session
from ..password import get_password_hash
from ..auth.jobseeker_auth import get_current_jobseeker


jobseeker_router = APIRouter()

@jobseeker_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    job_seeker = authenticate_jobseeker(form_data.username, form_data.password)
    if not job_seeker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": job_seeker.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



# Job seeker CRUD

# Create Jobseeker
@jobseeker_router.post("/jobseekers/", response_model=JobSeekerPublic)
def create_jobseeker(
    jobseeker: JobSeekerCreate,
    session: Session = Depends(get_session),
):

    hashed_password = get_password_hash(jobseeker.password)
    db_jobseeker = JobSeeker(**jobseeker.model_dump(),
                             hashed_password=hashed_password)
    session.add(db_jobseeker)
    session.commit()
    session.refresh(db_jobseeker)
    return db_jobseeker


# Get Jobseeker by ID
@jobseeker_router.get("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
def read_jobseeker(
    jobseeker_id: int,
    session: Session = Depends(get_session),
    current_user: JobSeeker = Depends(get_current_jobseeker)
):
    jobseeker = session.get(JobSeeker, jobseeker_id)
    if not jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    return jobseeker


# Get all Jobseekers
@jobseeker_router.get("/jobseekers/", response_model=list[JobSeekerPublic])
def read_jobseekers(session: Session = Depends(get_session), current_user: JobSeeker = Depends(get_current_jobseeker)):
    jobseekers = session.exec(select(JobSeeker)).all()
    return jobseekers


# Update Jobseeker by ID
@jobseeker_router.patch("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
def update_jobseeker(
    jobseeker_id: int,
    jobseeker_update: JobSeekerUpdate,
    session: Session = Depends(get_session),
    current_user: JobSeeker = Depends(get_current_jobseeker)
):
    if current_user.id != jobseeker_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this profile")

    jobseeker_db = session.get(JobSeeker, jobseeker_id)

    if not jobseeker_db:
        raise HTTPException(status_code=404, detail='jobseeker not found')

    jobseeker_data = jobseeker_update.model_dump(exclude_unset=True)
    jobseeker_db.sqlmodel_update(jobseeker_data)

    session.add(jobseeker_db)
    session.commit()
    session.refresh(jobseeker_db)

    return jobseeker_db


# Delete Jobseeker by ID
@jobseeker_router.delete("/jobseekers/{jobseeker_id}")
def delete_jobseeker(
    jobseeker_id: int,
    session: Session = Depends(get_session),
    current_user: JobSeeker = Depends(get_current_jobseeker)
):
    db_jobseeker = session.get(JobSeeker, jobseeker_id)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    session.delete(db_jobseeker)
    session.commit()
    return {"message": "Job seeker deleted successfully"}

