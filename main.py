from fastapi import FastAPI, HTTPException, Depends
from .database import engine
from sqlmodel import SQLModel, Session, select
from .models import JobSeeker, JobSeekerUpdate, JobSeekerCreate, JobSeekerPublic, Employer, EmployerCreate, EmployerPublic, EmployerUpdate

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


@app.post("/employers/", response_model=EmployerPublic)
def create_employer(*, session: Session = Depends(get_session), employer: EmployerCreate):
    # Check if email already exists
    existing_employer = session.exec(select(Employer).where(
        Employer.email == employer.email)).first()
    if existing_employer:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(employer.password)

    # Create the employer
    db_employer = Employer.model_validate(
        employer, update={"hashed_password": hashed_password})
    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer

# Read All Employers


@app.get("/employers/", response_model=list[EmployerPublic])
def read_employers(*, session: Session = Depends(get_session)):
    employers = session.exec(select(Employer)).all()
    return employers

# Read Single Employer


@app.get("/employers/{employer_id}", response_model=EmployerPublic)
def read_employer(*, session: Session = Depends(get_session), employer_id: int):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer

# Update Employer


@app.patch("/employers/{employer_id}", response_model=EmployerPublic)
def update_employer(*, session: Session = Depends(get_session), employer_id: int, employer: EmployerUpdate):
    db_employer = session.get(Employer, employer_id)
    if not db_employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    # Update fields if provided
    if employer.company_name:
        db_employer.company_name = employer.company_name
    if employer.email:
        db_employer.email = employer.email
    if employer.password:
        db_employer.hashed_password = pwd_context.hash(employer.password)

    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer

# Delete Employer


@app.delete("/employers/{employer_id}")
def delete_employer(*, session: Session = Depends(get_session), employer_id: int):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    session.delete(employer)
    session.commit()
    return None
