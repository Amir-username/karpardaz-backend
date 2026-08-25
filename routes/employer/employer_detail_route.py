from fastapi import APIRouter, Depends
from sqlmodel import Session

from ...auth.employer_auth import get_current_employer
from ...models.Employer import Employer
from ...models.EmployerDetail import EmployerDetail, EmployerDetailCreate, EmployerDetailUpdate
from ...session.session import get_session
from ...logic.employer_logic import (
    create_detail,
    get_detail,
    get_all_details,
    update_detail,
    remove_detail,
)

employer_detail_router = APIRouter()


@employer_detail_router.post('/employer-detail/', response_model=EmployerDetail)
def create_employer_detail(
    detail: EmployerDetailCreate,
    employer: Employer = Depends(get_current_employer),
    session: Session = Depends(get_session)
):
    return create_detail(session, detail, employer)


@employer_detail_router.get('/employer-detail/{id}', response_model=EmployerDetail)
def read_employer_detail(id: int, session: Session = Depends(get_session)):
    return get_detail(session, id)


@employer_detail_router.get('/employer-details/', response_model=list[EmployerDetail])
def read_all_employers(session: Session = Depends(get_session)):
    return get_all_details(session)


@employer_detail_router.patch('/employer-detail/{id}', response_model=EmployerDetail)
def update_employer_detail(
    id: int,
    employer_update: EmployerDetailUpdate,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    return update_detail(session, id, employer_update, employer)


@employer_detail_router.delete('/employer-detail/{id}')
def delete_employer_detail(
    id: int,
    session: Session = Depends(get_session),
    employer: Employer = Depends(get_current_employer)
):
    return remove_detail(session, id, employer)

