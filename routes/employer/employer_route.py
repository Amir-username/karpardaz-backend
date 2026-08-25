from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer, EmployerCreate, EmployerPublic, EmployerUpdate
from sqlmodel import Session
from ...session.session import get_session
from ...logic.employer_logic import (
    login_employer,
    register_employer,
    get_employers_list,
    get_employer,
    update_employer,
    remove_employer,
)

employer_router = APIRouter()


@employer_router.post("/employer/login")
async def login_for_access_token_employer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return login_employer(form_data)


@employer_router.post("/employers/", response_model=EmployerPublic)
def create_employer(*, session: Session = Depends(get_session), employer: EmployerCreate):
    return register_employer(session, employer)


@employer_router.get("/employers/")
def read_employers(*, session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    return get_employers_list(session, offset, limit)


@employer_router.get("/employers/{employer_id}", response_model=EmployerPublic)
def read_employer(*, session: Session = Depends(get_session), employer_id: int):
    return get_employer(session, employer_id)


@employer_router.patch("/employers/{employer_id}", response_model=EmployerPublic)
def update_employer_endpoint(
    *, session: Session = Depends(get_session), employer_id: int,
    employer: EmployerUpdate, current_user: Employer = Depends(get_current_employer)
):
    return update_employer(session, employer_id, employer, current_user)


@employer_router.delete("/employers/{employer_id}")
def delete_employer_endpoint(
    *, session: Session = Depends(get_session), employer_id: int,
    current_user: Employer = Depends(get_current_employer)
):
    return remove_employer(session, employer_id, current_user)

