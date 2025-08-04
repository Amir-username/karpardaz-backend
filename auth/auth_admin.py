from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from ..database import engine
from ..models.AdminUser import Admin
from ..core.password import verify_password
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status, Request
from ..session.session import get_session
from ..config import SECRET_KEY, ALGORITHM
from .token import TokenData
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError
from ..models.Employer import Employer
from ..models.JobSeeker import JobSeeker
from ..auth.employer_auth import oauth2_scheme_employer, get_current_employer
from ..auth.jobseeker_auth import oauth2_scheme_jobseeker, get_current_jobseeker


oauth2_scheme_admin = OAuth2PasswordBearer(
    tokenUrl="admin/login", scheme_name="admin authentication")


def authenticate_admin(username: str, password: str):
    with Session(engine) as session:
        admin = session.exec(select(Admin).where(
            Admin.username == username)).first()
        if not admin:
            return False
        if not verify_password(password, admin.hashed_password):
            return False
        return admin


def get_current_admin(
        token: Annotated[str, Depends(oauth2_scheme_admin)],
        session: Session = Depends(get_session)
):
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

    admin = session.exec(select(Admin).where(
        Admin.username == token_data.username)).first()

    if admin is None:
        raise credentials_exception
    return admin


async def get_current_employer_or_admin(
    request: Request,
    session: Session = Depends(get_session)
) -> Union[Employer, Admin]:
    """
    Returns authenticated user (either Employer or Admin) 
    with valid credentials
    """
    try:
        admin_token = oauth2_scheme_admin(request)
        admin = await get_current_admin(admin_token, session)
        return admin
    except HTTPException:
        pass

    try:
        employer_token = oauth2_scheme_employer(request)
        employer = await get_current_employer(employer_token, session)
        return employer
    except HTTPException:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )




async def get_current_jobseeker_or_admin(
    request: Request,
    session: Session = Depends(get_session)
) -> Union[JobSeeker, Admin]:
    """
    Returns authenticated user (either Employer or Admin) 
    with valid credentials
    """
    try:
        admin_token = oauth2_scheme_admin(request)
        admin = await get_current_admin(admin_token, session)
        return admin
    except HTTPException:
        pass 

    try:
        jobseeker_token = oauth2_scheme_jobseeker(request)
        jobseeker = await get_current_jobseeker(jobseeker_token, session)
        return jobseeker
    except HTTPException:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

