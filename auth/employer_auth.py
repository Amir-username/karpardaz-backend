from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from ..database import engine
from ..models.Employer import Employer
from ..core.password import verify_password
from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..session.session import get_session
from ..config import SECRET_KEY, ALGORITHM
from .token import TokenData
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError


oauth2_scheme_employer = OAuth2PasswordBearer(
    tokenUrl="employer/login", scheme_name="employer authentication")


def authenticate_employer(email: str, password: str):
    with Session(engine) as session:
        employer = session.exec(select(Employer).where(
            Employer.email == email)).first()
        if not employer:
            return False
        if not verify_password(password, employer.hashed_password):
            return False
        return employer


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
