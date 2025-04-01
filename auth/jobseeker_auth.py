from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..database import engine
from ..models.JobSeeker import JobSeeker
from ..password import verify_password
from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..session.session import get_session
from ..config import SECRET_KEY, ALGORITHM
from .token import TokenData
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError


oauth2_scheme_jobseeker = OAuth2PasswordBearer(
    tokenUrl="jobseeker/login", scheme_name="jobseeker authentication")


def authenticate_jobseeker(email: str, password: str):
    with Session(engine) as session:
        job_seeker = session.exec(select(JobSeeker).where(
            JobSeeker.email == email)).first()
        if not job_seeker:
            return False
        if not verify_password(password, job_seeker.hashed_password):
            return False
        return job_seeker
    

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
