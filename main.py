# username=amirnaji@example.com password=123456789
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import engine
from sqlmodel import SQLModel, Session, select
from .models import JobSeeker, JobSeekerUpdate, JobSeekerCreate, JobSeekerPublic, Employer, EmployerCreate, EmployerPublic, EmployerUpdate
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from jwt import decode as jwt_decode, encode as jwt_encode


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#### Password Hashing ####
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()
router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


##### AUTHENTICATION #####
oauth2_scheme_jobseeker = OAuth2PasswordBearer(
    tokenUrl="token", scheme_name="jobseeker authentication")
oauth2_scheme_employer = OAuth2PasswordBearer(
    tokenUrl="employer-token", scheme_name="employer authentication")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def authenticate_jobseeker(email: str, password: str):
    with Session(engine) as session:
        job_seeker = session.exec(select(JobSeeker).where(
            JobSeeker.email == email)).first()
        if not job_seeker:
            return False
        if not verify_password(password, job_seeker.hashed_password):
            return False
        return job_seeker


def authenticate_employer(email: str, password: str):
    with Session(engine) as session:
        employer = session.exec(select(Employer).where(
            Employer.email == email)).first()
        if not employer:
            return False
        if not verify_password(password, employer.hashed_password):
            return False
        return employer


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_jobseeker(token: Annotated[str, Depends(oauth2_scheme_jobseeker)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    job_seeker = session.exec(select(JobSeeker).where(
        JobSeeker.email == token_data.username)).first()

    if job_seeker is None:
        raise credentials_exception
    return job_seeker


def get_current_employer(token: Annotated[str, Depends(oauth2_scheme_employer)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    employer = session.exec(select(Employer).where(
        Employer.email == token_data.username)).first()

    if employer is None:
        raise credentials_exception
    return employer


@app.post("/token")
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


@app.post("/employer-token")
async def login_for_access_token_employer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    employer = authenticate_employer(form_data.username, form_data.password)
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": employer.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# Job seeker CRUD

# Create Jobseeker
@app.post("/jobseekers/", response_model=JobSeekerPublic)
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
@app.get("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
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
@app.get("/jobseekers/", response_model=list[JobSeekerPublic])
def read_jobseekers(session: Session = Depends(get_session), current_user: JobSeeker = Depends(get_current_jobseeker)):
    jobseekers = session.exec(select(JobSeeker)).all()
    return jobseekers


# Update Jobseeker by ID
@app.patch("/jobseekers/{jobseeker_id}", response_model=JobSeekerPublic)
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
@app.delete("/jobseekers/{jobseeker_id}")
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


# Employer CRUD

# Create Employer
@app.post("/employers/", response_model=EmployerPublic)
def create_employer(*, session: Session = Depends(get_session), employer: EmployerCreate):
    # Check if email already exists
    existing_employer = session.exec(select(Employer).where(
        Employer.email == employer.email)).first()
    if existing_employer:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(employer.password)

    # Create the employer
    db_employer = Employer.model_validate(
        employer, update={"hashed_password": hashed_password})
    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer


# Get all Employers
@app.get("/employers/", response_model=list[EmployerPublic])
def read_employers(*, session: Session = Depends(get_session), current_user: Employer = Depends(get_current_employer)):
    employers = session.exec(select(Employer)).all()
    return employers


# Ger Employer by ID
@app.get("/employers/{employer_id}", response_model=EmployerPublic)
def read_employer(*, session: Session = Depends(get_session), employer_id: int, current_user: Employer = Depends(get_current_employer)):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


# Update Employer by ID
@app.patch("/employers/{employer_id}", response_model=EmployerPublic)
def update_employer(*, session: Session = Depends(get_session), employer_id: int, employer: EmployerUpdate,
                    current_user: Employer = Depends(get_current_employer)):

    if current_user.id != employer_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this profile")

    db_employer = session.get(Employer, employer_id)
    if not db_employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    # Update fields if provided
    if employer.company_name:
        db_employer.company_name = employer.company_name
    if employer.email:
        db_employer.email = employer.email
    if employer.password:
        db_employer.hashed_password = get_password_hash(employer.password)

    session.add(db_employer)
    session.commit()
    session.refresh(db_employer)
    return db_employer


# Delete Employer by ID
@app.delete("/employers/{employer_id}")
def delete_employer(*, session: Session = Depends(get_session), employer_id: int, current_user: Employer = Depends(get_current_employer)):
    employer = session.get(Employer, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    session.delete(employer)
    session.commit()
    return None


app.include_router(router)
