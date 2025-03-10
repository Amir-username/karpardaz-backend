from fastapi import FastAPI, HTTPException, Depends
from .database import engine
from sqlmodel import SQLModel, Session, select
from .models import JobSeeker, JobSeekerUpdate, JobSeekerCreate, JobSeekerPublic

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/jobseekers/", response_model=JobSeekerPublic)
def create_jobseeker(
    jobseeker: JobSeekerCreate,
    session: Session = Depends(get_session)
):
    hashed_password = pwd_context.hash(jobseeker.password)
    db_jobseeker = JobSeeker(**jobseeker.model_dump(),
                             hashed_password=hashed_password)
    session.add(db_jobseeker)
    session.commit()
    session.refresh(db_jobseeker)
    return db_jobseeker


@app.get("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
def read_jobseeker(
    jobseeker_id: int,
    session: Session = Depends(get_session)
):
    jobseeker = session.get(JobSeeker, jobseeker_id)
    if not jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    return jobseeker


@app.get("/jobseekers/", response_model=list[JobSeekerPublic])
def read_jobseekers(session: Session = Depends(get_session)):
    jobseekers = session.exec(select(JobSeeker)).all()
    return jobseekers


@app.patch("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
def update_jobseeker(
    jobseeker_id: int,
    jobseeker_update: JobSeekerUpdate,
    session: Session = Depends(get_session)
):
    jobseeker_db = session.get(JobSeeker, jobseeker_id)

    if not jobseeker_db:
        raise HTTPException(status_code=404, detail='jobseeker not found')

    jobseeker_data = jobseeker_update.model_dump(exclude_unset=True)
    jobseeker_db.sqlmodel_update(jobseeker_data)

    session.add(jobseeker_db)
    session.commit()
    session.refresh(jobseeker_db)

    return jobseeker_db


@app.delete("/jobseekers/{jobseeker_id}")
def delete_jobseeker(
    jobseeker_id: int,
    session: Session = Depends(get_session)
):
    db_jobseeker = session.get(JobSeeker, jobseeker_id)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    session.delete(db_jobseeker)
    session.commit()
    return {"message": "Job seeker deleted successfully"}
