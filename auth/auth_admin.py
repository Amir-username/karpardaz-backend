from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from ..database import engine
from ..models.AdminUser import Admin
from ..password import verify_password
from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..session.session import get_session
from ..config import SECRET_KEY, ALGORITHM
from .token import TokenData
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError


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
